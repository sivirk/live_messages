# -*- coding: UTF-8

import datetime

from django.db import models
from django.contrib.auth.models import Group, User
from django.contrib.contenttypes.models import ContentType

from registers.helpers import get_sub_models


def get_tag_ct():
    return map(lambda ct: ct.pk, get_sub_models(Tag))


class Tag(models.Model):
    """ Теги для сообщений
    """

    content_type = models.ForeignKey(ContentType, verbose_name=u'Тип',
                                     editable=False,)
    title = models.CharField(max_length=255, verbose_name=u'Заголовок',
                             editable=False,)

    class Meta:
        verbose_name = u"тег"
        verbose_name_plural = u"теги"

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """ Устанавливаем тип и заголовок для тега """
        self.content_type = ContentType.objects.get_for_model(self)
        self.title = unicode(self)
        return super(Tag, self).save(*args, **kwargs)


class Register(models.Model):
    """ Журналы сообщений """

    title = models.CharField(max_length=255, verbose_name=u'Название')
    slug = models.SlugField(max_length=255, verbose_name=u'Slug')
    groups = models.ManyToManyField(Group, verbose_name=u'Для групп',
                                    null=True, blank=True)
    content_types = models.ManyToManyField(ContentType,
                                           verbose_name=u'Типы данных',
                                           null=True, blank=True,
                                           limit_choices_to={
                                               'id__in': get_tag_ct()
                                           })
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
