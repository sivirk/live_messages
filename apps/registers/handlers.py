# -*- coding: UTF-8 -*-

""" Работа с сообщениями
"""

from transport.helpers import MessageHandler
from registers.al_models import Message, Tag, Dairy


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

    PURPOSE = {
        'event': 1,
        'announce': 2,
        'description': 3,
    }

    class Meta:
        tags = ['message']
        model = Message
        save_props = ['id']

    def get_object_data(self, client, data):
        kwargs = data.copy()
        kwargs['purpose'] = self.PURPOSE.get(str(kwargs['purpose']))
        kwargs['user_id'] = client.user['_auth_user_id']

        tags = []
        tags_qs = self.controller.al_session.query(Tag)
        for tag in kwargs['tags']:
            tags.append(tags_qs)
        del kwargs['tags']
        kwargs['tags'] = tags
        return kwargs


class DairyHandler(MessageHandler):

    class Meta:
        tags = ['dairy']
        model = Dairy
