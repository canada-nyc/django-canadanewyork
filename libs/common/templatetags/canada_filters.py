import json

from django import template
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.template.defaultfilters import stringfilter
from django.conf import settings

register = template.Library()


@register.filter
@stringfilter
def escapejson(value):
    return mark_safe(json.dumps(force_text(value), ensure_ascii=False))


@register.filter
@stringfilter
def setting(value):
    return getattr(settings, value)
