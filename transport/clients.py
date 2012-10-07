# -*- coding: UTF-8 -*-


class ClientManager(object):
    """ Менеджер клиентов к торнадо
    """

    connections = {}

    def __getitem__(self, key):
        return self.connections[key]

    def append(self, client, info):
        """ Добавляем нового клиента """
        if client not in self.connections.keys():
            self.connections[client] = {'info': info}

    def remove(self, client):
        """ Удаление клиента """
        if client in self.connections.keys():
            del self.connections[client]
