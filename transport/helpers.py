# -*- coding: UTF-8 -*-

from django.utils import six

REGISTRY = {}


class OptionDoesNotExist(Exception):
    pass

KEYS = ['db_table']


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

        if hasattr(attr_meta, 'db_table'):
            kwargs['db_table'] = getattr(attr_meta, 'db_table')

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

    def handle(self, client, tag, data, result_data):
        if self._meta.db_table:
            # Если нет данных то поиск по полям
            if not data:
                return self.db.query("""
                    select title, slug from registers_register
                """)
            else:
                where = " and ".join(map(
                    lambda x: "%s='%s'" % (x[0], x[1]),
                    data.items())
                )
                return self.db.query("""
                    select title, slug from registers_register where %s
                """ % where)

    def handle_post(self, client, tag, data, result_data):
        """ Обработка POST метода
            создание новой записи в таблице
        """
        return {'id': 123, 'created': 'asdas'}
