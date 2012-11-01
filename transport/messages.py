# -*- coding: UTF-8 -*-

import json

from django.utils.importlib import import_module
from tornado import gen

from main import settings
from transport.helpers import REGISTRY
from base import BaseController


def json_converter(o):
    if hasattr(o, 'to_json'):
        return o.to_json()


class MessageManager(BaseController):
    """ Обработка входящих сообщений
        от клиента
    """

    _handlers = {}

    def __init__(self, application, handler):
        super(MessageManager, self).__init__(application, handler)
        for app in settings.INSTALLED_APPS:
            if not app.startswith('django'):
                try:
                    import_module("%s.handlers" % app)
                except ImportError:
                    pass
        self.update_handlers()

    def update_handlers(self,):
        """ Обновляет таблицу обработки сообщений """

        for name, handler in REGISTRY.items():
            for tag in handler._meta.tags:
                if not tag in self._handlers:
                    self._handlers[tag] = []
                self._handlers[tag].append((name, handler(self)))

    @gen.engine
    def handle_message(self, client, message,):
        """ Обрабатываем входящее сообщение """
        data = json.loads(message)
        result = {}
        tags = data.pop('tags')

        def wrapper(*args, **kwargs):
            callback = kwargs.pop('callback')
            for tag in tags:
                result.update(self.process_tag(client,
                              tag, data['params'], result))
            callback(result)

        result = yield gen.Task(wrapper)
        if result:
            self.handler.send(json.dumps(result, default=json_converter))

    def process_tag(self, client, tag, data, result):
        """ Обрабатываем тег """
        if not tag in result:
            result[tag] = None

        handlers = self._handlers.get(tag)
        if handlers:
            for name, handler in handlers:
                result[tag] = handler(client, tag, data, result)
        return result

    def error_message(self, tags='exception', message=None):
        """ Возвращает сообщение об ощибке для специального
            callback`а
        """

        result = {
            tags: {
                'message': message
            }
        }
        return json.dumps(result)
