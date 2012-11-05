# -*- coding: UTF-8 -*-

import os
import json

from django.views.generic import TemplateView
from django.conf import settings


class ApplicationMixin(TemplateView):
    """ mixin для всех приложений
    """

    # Библиотеки для работы приложения
    libs = []
    # Приложения в которых искать less и coffee
    apps = []

    def get_files(self, path, file_type):
        """ Возвращает все файлы указанного типа
        """
        files = []

        for dirname, dirnames, filenames in os.walk(path):
            files += filter(lambda x: x.endswith(file_type), filenames)
            # @todo: Проход по поддиректориям

        return files

    def get_app_libs(self, app):
        """ Возвращает список библиотек прилодения """
        less = []
        libs = []

        app_name = app.split(".").pop()
        app_path = app if app == 'main' else 'apps/%s' % app
        path = os.path.join(settings.BASE_PATH, "..",
                            app_path)

        less_path = os.path.join(path, "static", app_name, "less")
        coffee_path = os.path.join(path, "coffee")

        if os.path.exists(less_path):
            less = self.get_files(less_path, 'less')
            less = map(lambda l: self.create_media_path(app, 'less', l), less)

        if os.path.exists(coffee_path):
            coffee = self.get_files(coffee_path, 'coffee')
            js = map(lambda x: x.replace(".coffee", ".js"), coffee)
            libs += map(lambda l: self.create_media_path('js', app, l), js)

        return {'less': less, 'libs': libs}

    def create_media_path(self, *args):
        return os.path.join(settings.STATIC_URL, *args)

    def get_media(self,):
        """ Получает список всех медиа библиотек """

        libs = []
        less = []
        apps = []

        libs += map(lambda l: self.create_media_path('libs', l), self.libs)

        for app in self.apps:
            files = self.get_app_libs(app)
            apps += files.get('libs', [])
            less += files.get('less', [])

        return {'libs': json.dumps(libs), 'less': less, 'apps': apps}

    def get_context_data(self, **kwargs):
        kwargs['settings'] = json.dumps({
            'transport': settings.TRANSPORT_SERVER,
            'debug': settings.DEBUG,
        })
        kwargs['title'] = 'Журналы'
        kwargs['media'] = self.get_media()
        kwargs['debug'] = settings.DEBUG
        return super(ApplicationMixin, self).get_context_data(**kwargs)


class HomeView(ApplicationMixin, TemplateView):

    template_name = "main/index.html"

    apps = [
        'main',
        'registers',
        'stations',
        'utils',
        'users',
    ]

    libs = [
        # Основные библиотеки
        'sockjs-0.3.min.js',
        'jquery-1.8.2.min.js',
        'mustache.js',
        'jquery-ui/jquery-ui-1.9.0.min.js',
        'jquery-ui/smoothness/jquery-ui-1.9.0.min.css',
        'bootstrap/js/bootstrap.min.js',
        'bootstrap/css/bootstrap.min.css',
        'bootstrap/css/bootstrap-responsive.min.css',

        # Spine
        'spine/spine.js',
        'spine/route.js',
    ]

home = HomeView.as_view()
