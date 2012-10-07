# -*- coding: UTF-8 -*-

import json

from tornado import web, ioloop
from sockjs.tornado import SockJSRouter, SockJSConnection


class EchoConnection(SockJSConnection):

    participants = set()

    def on_open(self, info):
        print 'connected'

    def on_message(self, msg):
        print msg
        # self.send(msg)

    def on_close(self):
        print 'opaaa'

if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    EchoRouter = SockJSRouter(EchoConnection, '/updater')

    app = web.Application(EchoRouter.urls)
    app.listen(9999)
    ioloop.IOLoop.instance().start()
