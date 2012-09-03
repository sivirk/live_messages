# -*- coding: utf-8 -*-

import uwsgi
from uwsgidecorators import timer
from django.utils import autoreload

@timer(1)
def change_code_gracefull_reload(sig):
    if autoreload.code_changed():
        uwsgi.reload()

#django_wsgi.py
import os
import sys
import warnings

current = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([current, os.path.join(current, '../')])


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

#from utils.wsgi import LogWSGIHandler
#application = LogWSGIHandler()

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()