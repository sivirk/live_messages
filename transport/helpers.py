# -*- coding: UTF-8 -*-

from django.utils import six

REGISTRY = {}


class Options():

    tags = []

    def __init__(self, tags,):
        self.tags = tags


class MessageHandlerMeta(type):

    def __new__(cls, name, bases, attrs):
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

    def __call__(self, tag, data, result_data):
        return self.handle(tag, data, result_data)

    def handle(self, tag, data, result_data):
        raise NotImplementedError
