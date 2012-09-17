# -*- coding: utf-8 -*-

from django.db import models

from registers.models import Tag


class Station(Tag):
    """ Все станции АТС,
        а также ПСЭ """

    TYPE_MAIN = 1
    TYPE_SUB = 2

    TYPE_CHOICES = ((TYPE_MAIN, u'АТС'),
                    (TYPE_SUB, u'ПСЭ'),)

    type = models.SmallIntegerField(verbose_name=u'Оборудорвание',
                                    choices=TYPE_CHOICES)
    name = models.CharField(max_length=255, verbose_name=u'Название')
    subscribers = models.IntegerField(verbose_name=u'Количество абонентов',
                                      null=True, blank=True)
    vendor = models.CharField(max_length=255, verbose_name=u'Производитель')
    description = models.TextField(verbose_name=u'Описание',
                                   help_text=u'Адрес, доп инфо, ключи',
                                   blank=True)

    class Meta:
        verbose_name = u'станция'
        verbose_name_plural = u'объекты'

    def __unicode__(self):
        return self.name

# Межстанционные связи и абоненты
# -------------------------------


class Route(Tag):
    """ Направления """

    name = models.CharField(max_length=255, verbose_name=u'Название')
    station = models.ForeignKey(Station, verbose_name=u'Станция')
    signaling = models.CharField(max_length=255, verbose_name=u'Сигнализация',
                                 blank=True,)
    channels = models.IntegerField(verbose_name=u'Всего каналов',
                                   null=True, blank=True)
    description = models.TextField(verbose_name=u'Описание',
                                   blank=True)

    class Meta:
        verbose_name = u'направление'
        verbose_name_plural = u'направления'

    def __unicode__(self):
        return self.name


class Subscriber(Tag):
    """ Абонеты станций,
        УПАТС, такси, вирт. номера,
        осн. серийных групп """

    number = models.BigIntegerField(verbose_name=u'Номер')
    station = models.ForeignKey(Station, verbose_name=u'Станция')
    description = models.TextField(verbose_name=u'Описание',
                                   blank=True)

    class Meta:
        verbose_name = u'абонент'
        verbose_name_plural = u'абоненты'

    def __unicode__(self):
        return self.number

# Оборудование
# -------------------------------


class Equipment(Tag):
    """ Станционное оборудование:
        - стативы
        - платы
        - и т.д.
    """
    name = models.CharField(max_length=255, verbose_name=u'Название')
    station = models.ForeignKey(Station, verbose_name=u'Станция')
    subscribers = models.IntegerField(verbose_name=u'Абоненты',
                                      help_text='''Кол-во обслуживаемых
                                                   абонентов''',
                                      null=True, blank=True)
    description = models.TextField(verbose_name=u'Описание',
                                   blank=True)

    class Meta:
        verbose_name = u'оборудование'
        verbose_name_plural = u'оборудование'

    def __unicode__(self):
        return self.name
