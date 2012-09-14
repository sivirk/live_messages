# -*- coding: utf-8 -*-

import uwsgi
from django.utils import autoreload


import os
import sys

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_PATH, "../libs/"))

from uwsgidecorators import timer


@timer(1)
def change_code_gracefull_reload(sig):
    if autoreload.code_changed():
        uwsgi.reload()

#django_wsgi.py
import os
import sys

current = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([current, os.path.join(current, '../')])


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

#from utils.wsgi import LogWSGIHandler
#application = LogWSGIHandler()

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
