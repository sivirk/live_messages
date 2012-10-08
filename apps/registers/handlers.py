# -*- coding: UTF-8 -*-

""" Работа с сообщениями
"""

from transport.helpers import MessageHandler


class AutocompleteHandler(MessageHandler):
    """ Обработчик для автокомплита сообщений """

    class Meta:
        tags = ['autocomplete']

    def handle(self, tag, data, result_data):
        return ["OPPPA", "GOPPA"]


class MessageHandler(MessageHandler):
    """ Обработчик для сообщений """

    class Meta:
        tags = ['message']
