from django import template
from pudb import set_trace


register = template.Library()


@register.filter
def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""
    if hasattr(value, arg):
        return getattr(value, arg)


@register.filter
def pudb(element):
    set_trace()
    return element
