# -*- coding: utf-8 -*-

from django.contrib import admin

from stations.models import Station, Route, \
                            Subscriber, Equipment


class StationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'type', 'vendor', 'subscribers')

admin.site.register(Station, StationAdmin)


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'station')

admin.site.register([Route, Subscriber, Equipment], EquipmentAdmin)
