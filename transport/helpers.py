# -*- coding: UTF-8 -*-

from django.utils import six

REGISTRY = {}
MODEL_ATTRS = ['db_table', 'model', 'list_props', 'save_props', 'order_by']


class OptionDoesNotExist(Exception):
    pass


class Options():

    tags = []

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class MessageHandlerMeta(type):

    def __new__(cls, name, bases, attrs):
        global REGISTRY
        super_new = super(MessageHandlerMeta, cls).__new__
        parents = [b for b in bases if isinstance(b, MessageHandlerMeta) and
                   not (b.__name__ == 'NewBase' and b.__mro__ == (b, object))]
        if not parents:
            return super_new(cls, name, bases, attrs)

        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})

        attr_meta = attrs.pop('Meta', None)

        kwargs = {}
        kwargs['tags'] = getattr(attr_meta, 'tags')

        for attr in MODEL_ATTRS:
            kwargs[attr] = getattr(attr_meta, attr, None)

        setattr(new_class, "_meta", Options(**kwargs))
        for attr, value in attrs.items():
            if attr not in ['Meta', ]:
                setattr(new_class, attr, value)

        name = new_class.__name__.lower()
        if name not in REGISTRY.keys():
            REGISTRY[name] = new_class
        return new_class


class MessageHandler(six.with_metaclass(MessageHandlerMeta, object)):
    """ Базовый обработчик сообщений """

    def __init__(self, controller):
        self.controller = controller

    @property
    def db(self):
        return self.controller.db

    @property
    def asyncdb(self):
        return self.controller.asyncdb

    def __call__(self, client, tag, method, data, result_data):
        tag_method = tag.replace(".", "").replace(" ", "_")
        if hasattr(self, "handle_%s" % method):
            method = getattr(self, "handle_%s" % method)
            result = method(client, tag, data, result_data)
        elif hasattr(self, "handle_%s" % tag_method):
            method = getattr(self, "handle_%s" % tag_method)
            result = method(client, tag, data, result_data)
        else:
            result = self.handle(client, tag, data, result_data)

        if type(result) is bool:
            return {'success': result}
        return result

    def update_object_data(self, client, data):
        """ На основе переданных данных
            возвращает данные для нового объекта
        """
        return data

    def get_object_dict(self, obj, props=None):
        """ Возвращает словарь на основе данных
            объекта из запрошенных свойств
        """
        obj_dict = {}
        if not props:
            obj_dict = obj.__dict__.copy()
            del obj_dict['_sa_instance_state']
            obj_dict['unicode'] = unicode(obj)
        else:
            for prop in props:
                if hasattr(obj, prop):
                    value = getattr(obj, prop)
                    obj_dict[prop] = value
                elif prop == 'unicode':
                    obj_dict[prop] = unicode(obj)
        return obj_dict

    def handle(self, client, tag, data, result_data):
        if self._meta.model:
            qs = self.controller.al_session.query(self._meta.model)
            if data:
                # @TODO: Сделать фильтр!
                objects = qs.filter()
            else:
                objects = qs

            if self._meta.order_by is not None:
                objects = objects.order_by(self._meta.order_by)
            else:
                objects = objects.order_by(self._meta.model.id)

            # @todo: Выборка результатов должна быть в соответствии с
            #        необходимыми параметрами list_props
            result = []
            for o in objects:
                result.append(
                    self.get_object_dict(o, self._meta.list_props)
                )
            return result

    def handle_post(self, client, tag, data, result_data):
        """ Обработка POST метода
            создание новой записи в таблице
        """

        kwargs = self.update_object_data(client, data)
        if 'id' in kwargs:
            del kwargs['id']
        obj = self._meta.model(**kwargs)
        self.controller.al_session.add(obj)
        self.controller.al_session.commit()
        return self.get_object_dict(obj, self._meta.save_props)
