# -*- coding: UTF-8 -*-

import os
import sys

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_PATH, "../apps/"))
sys.path.append(os.path.join(BASE_PATH, "../"))

from tornado import web, ioloop
from sockjs.tornado import SockJSRouter, SockJSConnection

from messages import MessageManager
from clients import ClientManager


class ClientConnection(SockJSConnection):

    clients = ClientManager()
    messages = MessageManager()

    def on_open(self, info):
        self.clients.append(self, info)

    def on_message(self, msg):
        result = self.messages.handle_message(self.clients[self], msg)
        if result:
            self.send(result)

    def on_close(self):
        self.clients.remove(self)

if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    EchoRouter = SockJSRouter(ClientConnection, '/transport')

    app = web.Application(EchoRouter.urls,
                          debug=True)
    app.listen(9999)
    ioloop.IOLoop.instance().start()
