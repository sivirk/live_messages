# -*- coding: UTF-8 -*-

import logging
import os
import sys

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_PATH, "../apps/"))
sys.path.append(os.path.join(BASE_PATH, "../"))

from tornado import web, ioloop
from sockjs.tornado import SockJSRouter, SockJSConnection

from main import settings
from messages import MessageManager
from users.manager import ClientManager


class ClientConnection(SockJSConnection):

    def __init__(self, *args, **kwargs):
        super(ClientConnection, self).__init__(*args, **kwargs)
        self.clients = ClientManager(application=app, handler=self)
        self.messages = MessageManager(application=app, handler=self)

    def on_open(self, info):
        client = self.clients.append(self, info)
        if client and not client.user:
            return self.send(self.messages.error_message("auth.error"))

    def on_message(self, msg):
        client = self.clients[self]
        self.messages.handle_message(client, msg)

    def on_close(self):
        self.clients.remove(self)


class MessagedApplication(web.Application):
    """ Приложение сообщений """

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    EchoRouter = SockJSRouter(ClientConnection, '/transport')

    app = MessagedApplication(EchoRouter.urls,
                              debug=settings.DEBUG)

    logging.debug("Starting server on %s" % unicode(settings.TRANSPORT_SERVER))
    app.listen(**settings.TRANSPORT_SERVER)
    ioloop.IOLoop.instance().start()
