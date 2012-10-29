# -*- coding: UTF-8 -*-

import base64
import pickle
import datetime
import hmac
import hashlib

from main import settings
from base import BaseController
from users.client import Client
from users.hashers import PBKDF2PasswordHasher

BACKEND = 'django.contrib.auth.backends.ModelBackend'


class ClientManager(BaseController):
    """ Управление пользователями, авторизация
    """

    connections = {}

    def __getitem__(self, key):
        return self.connections[key]

    def authenticate(self, client, username, password):
        info = self.db.get("""
            select id, password from  auth_user where username=%s
        """, username)
        auth_data = {}
        hasher = PBKDF2PasswordHasher()

        if info and hasher.verify(password, info['password']):
            auth_data = {
                '_auth_user_id': info['id'],
                '_auth_user_backend': BACKEND,
            }
            client.user = auth_data
            data = self.encode(auth_data)
            session = client.info.cookies['sessionid'].value

            self.db.execute("""
                    update django_session set session_data="%s"
                    where session_key="%s"
                """ % (data, session))
        return bool(auth_data)

    def logout(self, client):
        session = client.info.cookies['sessionid'].value
        data = self.encode({})
        self.db.execute("""
                    update django_session set session_data="%s"
                    where session_key="%s"
            """ % (data, session))
        return True

    def get_user(self, session):
        """ Возвращает пользователя. """
        session = self.db.get("""
                        select * from django_session where session_key="%s"
                    """ % session)
        now = datetime.datetime.now()
        if session and session['expire_date'] > now:
            return self.decode(session['session_data'])

    def encode(self, session_dict):
        "Returns the given session dictionary pickled and encoded as a string."
        pickled = pickle.dumps(session_dict, pickle.HIGHEST_PROTOCOL)
        hash = self._hash(pickled)
        return base64.b64encode(hash.encode() + b":" + pickled).decode('ascii')

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
        if 'sessionid' in info.cookies:
            session = info.cookies['sessionid'].value
            try:
                user = self.get_user(session)
            except ValueError:
                user = None
            if client not in self.connections.keys():
                self.connections[client] = Client(**{
                    'info': info,
                    'user': user,
                    'manager': self,
                })
                return self.connections[client]

    def remove(self, client):
        """ Удаление клиента """
        if client in self.connections.keys():
            del self.connections[client]
