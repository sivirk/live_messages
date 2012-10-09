# -*- coding: UTF-8 -*-

""" Работа с сообщениями
"""

from transport.helpers import MessageHandler


class AutocompleteHandler(MessageHandler):
    """ Обработчик для автокомплита сообщений """

    class Meta:
        tags = ['autocomplete']

    def handle(self, tag, data, result_data):
        q = data['request']
        return map(lambda l: l.get('title'),
                   self.db.query("""
                                    SELECT title FROM registers_tag
                                    where title like "%%s%"
                                 """, q))


class MessageHandler(MessageHandler):
    """ Обработчик для сообщений """

    class Meta:
        tags = ['message']
