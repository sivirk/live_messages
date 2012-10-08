# -*- coding: UTF-8 -*-

import json

from django.utils.importlib import import_module

from main import settings
from transport.helpers import REGISTRY


class MessageManager(object):
    """ Обработка входящих сообщений
        от клиента
    """

    _handlers = {}

    def __init__(self,):
        for app in settings.INSTALLED_APPS:
            if not app.startswith('django'):
                try:
                    import_module("%s.handlers" % app)
                except:
                    pass
        self.update_handlers()

    def update_handlers(self,):
        """ Обновляет таблицу обработки сообщений """

        for name, handler in REGISTRY.items():
            for tag in handler._meta.tags:
                if not tag in self._handlers:
                    self._handlers[tag] = []
                self._handlers[tag].append((name, handler()))

    def handle_message(self, client, message,):
        """ Обрабатываем входящее сообщение """
        data = json.loads(message)
        result = {}
        tags = data.pop('tags')
        for tag in tags:
            result.update(self.process_tag(tag, data, result))
        return json.dumps(result)

    def process_tag(self, tag, data, result):
        """ Обрабатываем тег """
        if not tag in result:
            result[tag] = None
            
        handlers = self._handlers.get(tag)
        if handlers:
            for name, handler in handlers:
                result[tag] = handler(tag, data, result)
        return result
