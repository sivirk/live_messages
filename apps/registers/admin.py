# -*- coding: utf-8 -*-

from django.contrib import admin

from registers.models import Register, Message


class RegisterAdmin(admin.ModelAdmin):
    """ Администрирование журналов """

    list_display = ('title',)

admin.site.register(Register, RegisterAdmin)


class MessageAdmin(admin.ModelAdmin):
    """ Администрирование журналов """

    list_display = ('text',)

admin.site.register(Message, MessageAdmin)

