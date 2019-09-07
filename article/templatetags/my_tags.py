# -*- coding: utf-8 -*-
# 'author':'hxy'

from django import template
register = template.Library()

@register.filter(name='movespace')
def mymovespace(value):
    return value.replace(' ','')
