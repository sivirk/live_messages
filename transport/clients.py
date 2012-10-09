# -*- coding: UTF-8 -*-

import base64
import pickle
import datetime
import hmac
import hashlib

from main import settings


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
        session = self.db.get("""
                        select * from django_session where session_key="%s"
                    """ % session)
        now = datetime.datetime.now()
        if session and session['expire_date'] > now:
            return self.decode(session['session_data'])

    def decode(self, session_data):
        encoded_data = base64.decodestring(session_data)
        try:
            # could produce ValueError if there is no ':'
            hash, pickled = encoded_data.split(':', 1)
            expected_hash = self._hash(pickled)
            if not self.constant_time_compare(hash, expected_hash):
                raise ValueError()
            else:
                return pickle.loads(pickled)
        except Exception:
            pass

    def _hash(self, value):
        key_salt = "django.contrib.sessionsSessionStore"

        return self.salted_hmac(key_salt, value,
                                settings.SECRET_KEY).hexdigest()

    def salted_hmac(self, key_salt, value, secret=None):
        key = hashlib.sha1(key_salt + secret).digest()

        return hmac.new(key, msg=value, digestmod=hashlib.sha1)

    def constant_time_compare(self, val1, val2):
        if len(val1) != len(val2):
            return False
        result = 0
        for x, y in zip(val1, val2):
            result |= ord(x) ^ ord(y)
        return result == 0

    def append(self, client, info):
        """ Добавляем нового клиента """
        session = info.cookies['sessionid'].value
        try:
            user = self.get_user(session)
        except ValueError:
            user = None
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
