# -*- coding: UTF-8

from django.db.models.loading import get_models
from django.contrib.contenttypes.models import ContentType


def get_sub_models(supermodel):
    """ Возвращает модели(ct)
        которые наследуются от supermodel """
    for model in get_models():
        if issubclass(model, supermodel):
            yield ContentType.objects.get_for_model(model)
