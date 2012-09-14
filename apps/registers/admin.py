# -*- coding: utf-8 -*-

from django.contrib import admin

from registers.models import Register


class RegisterAdmin(admin.ModelAdmin):
    """ Администрирование журналов """

    list_display = ('title',)

admin.site.register(Register, RegisterAdmin)
