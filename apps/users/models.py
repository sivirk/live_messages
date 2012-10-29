# -*- coding: UTF-8 -*-

from django.contrib.auth.models import User


class Profile(User):
    """ Новый пользователь с профилем """

    def __unicode__(self):
        if self.last_name or self.first_name:
            return "%s %s" % (self.last_name, self.first_name)
        else:
            return self.username

    def to_json(self):
        return {'user_id': self.pk,
                'user_name': unicode(self)}

    class Meta:
        verbose_name = u'пользователя'
        verbose_name_plural = u'пользователи'
