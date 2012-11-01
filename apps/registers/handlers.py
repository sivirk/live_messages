# -*- coding: UTF-8 -*-

""" Работа с сообщениями
"""

from tornado import gen

from transport.helpers import MessageHandler


class AutocompleteHandler(MessageHandler):
    """ Обработчик для автокомплита сообщений """

    class Meta:
        tags = ['autocomplete']

    def handle(self, client, tag, data, result_data):
        q = data['request']
        return map(lambda l: l.get('title'),
                   self.db.query("""
                                    SELECT title FROM registers_tag
                                    where title like "%%%%%s%%%%"
                                 """ % q))


class MessageHandler(MessageHandler):
    """ Обработчик для сообщений """

    class Meta:
        tags = ['message']


class DairyListHandler(MessageHandler):

    class Meta:
        tags = ['get_dairy_list']

    def handle(self, client, tag, data, result_data):
        return self.db.query( """
            select title, slug from registers_register
        """)
