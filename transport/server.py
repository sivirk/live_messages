# -*- coding: UTF-8 -*-

import os
import sys

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_PATH, "../apps/"))
sys.path.append(os.path.join(BASE_PATH, "../"))

from tornado import web, ioloop
from sockjs.tornado import SockJSRouter, SockJSConnection
import torndb

from main import settings
from messages import MessageManager
from clients import ClientManager


class ClientConnection(SockJSConnection):

    def __init__(self, *args, **kwargs):
        db_def = settings.DATABASES['default']
        db_host = "%s:%s" % (db_def.get("HOST", 'localhost') or 'localhost',
                             db_def.get("PORT", '3306') or '3306')
        self.db = torndb.Connection(
            host=db_host, database=db_def['NAME'],
            user=db_def['USER'], password=db_def['PASSWORD'])

        self.clients = ClientManager(self.db)
        self.messages = MessageManager(self.db)
        super(ClientConnection, self).__init__(*args, **kwargs)

    def on_open(self, info):

        client = self.clients.append(self, info)
        if client and not client['user']:
            return self.send(self.messages.error_message("auth.error"))

    def on_message(self, msg):

        client = self.clients[self]
        result = self.messages.handle_message(client, msg)

        if result:
            self.send(result)

    def on_close(self):
        self.clients.remove(self)

if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    EchoRouter = SockJSRouter(ClientConnection, '/transport')

    app = web.Application(EchoRouter.urls,
                          debug=settings.DEBUG)

    logging.debug("Starting server on %s" % unicode(settings.TRANSPORT_SERVER))
    app.listen(**settings.TRANSPORT_SERVER)
    ioloop.IOLoop.instance().start()
