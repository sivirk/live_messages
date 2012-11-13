# -*- coding: UTF-8 -*-

import torndb
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from main import settings


class BaseController(object):

    def __init__(self, application, handler):
        self.application = application
        self.handler = handler

    @property
    def al_session(self):
        if hasattr(self.application, 'al_session'):
            return getattr(self.application, 'al_session')

        db_settings = settings.DATABASES['default']
        engine = create_engine(
            'mysql://%(USER)s:%(PASSWORD)s@%(HOST)s/%(NAME)s' %
            db_settings, pool_recycle=3600, encoding='UTF-8',
            convert_unicode=True,)

        Session = sessionmaker(bind=engine)
        al_session = Session()
        al_session.execute("SET NAMES utf8")
        setattr(self.application, 'al_session', al_session)

        return self.application.al_session

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
