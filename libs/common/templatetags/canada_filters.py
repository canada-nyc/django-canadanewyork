import json
from urllib.parse import urljoin

from django import template
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
@stringfilter
def escapejson(value):
    return mark_safe(json.dumps(force_text(value), ensure_ascii=False))


@register.filter
@stringfilter
def setting(value):
    return getattr(settings, value)


@register.filter
@stringfilter
def absolute(value):
    print(get_current_site(None).domain)
    return urljoin(get_current_site(None).domain, value)
