# -*- coding: UTF-8 -*-

import json

from django.views.generic import TemplateView
from django.conf import settings


class HomeView(TemplateView):

    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        kwargs['settings'] = json.dumps({
            'transport': settings.TRANSPORT_SERVER,
            'debug': settings.DEBUG,
        })
        return super(HomeView, self).get_context_data(**kwargs)

home = HomeView.as_view()
