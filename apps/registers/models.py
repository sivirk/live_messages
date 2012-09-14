# -*- coding: UTF-8

import datetime

from django.db import models
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType

from register.helpers 


class Tag(models.Model):
    """ Теги для сообщений
        Все модели наследуются от этой
    """

    content_type = models.ForeignKey(ContentType, verbose_name=u'Тип',)
    title = models.CharField(max_length=255, verbose_name=u'Заголовок')

    class Meta:
        verbose_name = u"тег"
        verbose_name_plural = u"теги"

    def __unicode__(self):
        return self.title


class Register(models.Model):
    """ Журналы сообщений """

    title = models.CharField(max_length=255, verbose_name=u'Название')
    groups = models.ManyToManyField(Group, verbose_name=u'Для групп',
                                    null=True, blank=True)
    content_types = models.ManyToManyField(ContentType,
                                           verbose_name=u'Типы данных',
                                           null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=u'Теги',
                                  null=True, blank=True)

    class Meta:
        verbose_name = u"журнал"
        verbose_name_plural = u"журналы"

    def __unicode__(self):
        return self.title


class Message(models.Model):
    """ Сообщения, объявления, и т.д. """

    PURPOSE_EVENT = 1
    PURPOSE_ANNOUNCE = 2
    PURPOSE_DESCRIPTION = 3
    PURPOSE_CHOICES = ((PURPOSE_EVENT, u'Событие'),
                       (PURPOSE_ANNOUNCE, u'Объявление'),
                       (PURPOSE_DESCRIPTION, u'Описание'))

    created = models.DateTimeField(verbose_name=u'Дата создания',
                                   default=datetime.datetime.now)
    stamp = models.DateTimeField(verbose_name=u'Дата сообытия')
    purpose = models.SmallIntegerField(verbose_name=u'Назначение',
                                       choices=PURPOSE_CHOICES)
    user = models.ForeignKey(User, verbose_name=u'Автор')
    register = models.ForeignKey(Register,
                                 verbose_name=u'Основной журнал')
    text = models.TextField(verbose_name=u'Сообщение')
    tags = models.ManyToManyField(Tag, verbose_name=u'Теги',
                                  null=True)

    class Meta:
        verbose_name = u"сообщение"
        verbose_name_plural = u"сообщения"

    def __unicode__(self):
        pass
