# -*- coding: UTF-8 -*-

from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "main/home.html"

home = HomeView.as_view()
