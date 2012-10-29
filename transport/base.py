# -*- coding: UTF-8 -*-

import torndb
from main import settings


class BaseController(object):

    def __init__(self, application, handler):
        self.application = application
        self.handler = handler

    @property
    def db(self):
        if hasattr(self.application, 'db'):
            return getattr(self.application, 'db')

        db_settings = settings.DATABASES['default']
        db = torndb.Connection(
            host=db_settings['HOST'], database=db_settings['NAME'],
            user=db_settings['USER'], password=db_settings['PASSWORD'])

        setattr(self.application, 'db', db)

        return self.application.db
