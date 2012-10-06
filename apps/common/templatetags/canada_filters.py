from django import template
from django.conf import settings


register = template.Library()


@register.filter
def create_list(value):
    return [value]


@register.filter
def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""
    if hasattr(value, str(arg)):
        return getattr(value, arg)
