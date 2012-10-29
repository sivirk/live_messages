# -*- coding: UTF-8 -*-


class Client(object):
    """ Клиент """

    _info = {}

    def __init__(self, info, user, manager):
        self.user = user
        self.info = info
        self.manager = manager

    def is_authenticated(self):
        return bool(self.user.get('user_id', False))

    def __getattr__(self, key):

        if not self._info:
            self._info = self.manager.db.get("""
                select * from auth_user where id=%s
            """, self.user['_auth_user_id'])

        return self._info.get(key)

    def __unicode__(self,):
        if self.first_name or self.last_name:
            return u"%s %s" % (self.last_name, self.first_name)
        else:
            return u"%s" % self.username

    def __repr__(self):
        """ """
        return str(self.user)

    def to_json(self):
        """ """
        if self.user:
            result = {
                'user_id': unicode(self.user['_auth_user_id']),
                'user_name': unicode(self),
            }
        else:
            result = {}
        return result
