# -*- coding: UTF-8 -*-


class ClientManager(object):
    """ Менеджер клиентов к торнадо
    """

    connections = {}

    def __init__(self, db):
        self.db = db

    def __getitem__(self, key):
        return self.connections[key]

    def get_user(self, session):
        """ Возвращает пользователя. """

    def append(self, client, info):
        """ Добавляем нового клиента """
        session = info.cookies['sessionid'].value
        user = self.get_user(session)

        if client not in self.connections.keys():
            self.connections[client] = {
                'info': info,
                'user': user,
            }
            return self.connections[client]

    def remove(self, client):
        """ Удаление клиента """
        if client in self.connections.keys():
            del self.connections[client]
