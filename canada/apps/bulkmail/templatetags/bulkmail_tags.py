from django import template
from django.contrib.sites.models import Site

register = template.Library()


@register.filter
def full_domain(value):
    return '//' + Site.objects.get_current().domain + value
