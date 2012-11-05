# -*- coding: UTF-8 -*-

""" Разные утилиты
"""

import os

from django.utils.importlib import import_module

from transport.helpers import MessageHandler
from main import settings


class TemplateHandler(MessageHandler):
    """ Загрузчик шаблонов """

    class Meta:
        tags = ['templates']

    def handle(self, client, tag, data, result_data):
        name = data.get('name',)
        if not name.endswith(".html"):
            name = "%s.html" % name

        for app in settings.INSTALLED_APPS:
            if not app.startswith('django'):
                try:
                    app = import_module("%s" % app)
                    app_path = "/".join(app.__file__.split("/")[:-1])
                    template_path = os.path.join(app_path, "templates", name)
                    if os.path.exists(template_path):
                        return {'template': open(template_path).read()}
                except ImportError:
                    pass
        return False
