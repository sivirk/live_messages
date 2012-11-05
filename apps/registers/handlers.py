# -*- coding: UTF-8 -*-

""" Работа с сообщениями
"""

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
        db_table = 'register_message'


class DairyHandler(MessageHandler):

    class Meta:
        tags = ['dairy']
        db_table = 'register_registers'
