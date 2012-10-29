# -*- coding: UTF-8 -*-

import json

from django import template

register = template.Library()


def json_converter(o):
    if hasattr(o, 'to_json'):
        return o.to_json()


@register.filter
def to_json(value):
    """ Рендерит объект в json """
    return json.dumps(value, default=json_converter)
