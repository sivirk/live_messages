# -*- coding: UTF-8 -*-

from transport.helpers import MessageHandler


class AuthFormHandler(MessageHandler):
    """ Авторизация """

    class Meta:
        tags = ['.login-form form']

    def handle(self, client, tag, data, result_data):
        if not client.is_authenticated():
            if self.controller.handler.clients.authenticate(
                client, data['auth-username'],
                data['auth-password']
            ):
                return {'success': True, 'user': client}
            else:
                return {'success': False}


class LogOutHandler(MessageHandler):
    """ Выход """

    class Meta:
        tags = ['logout']

    def handle(self, client, tag, data, result_data):
        return {'success': self.controller.handler.clients.logout(client)}
