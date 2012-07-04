from django import template
from django.contrib.sites.models import Site


def do_domain(parser, token):
    return DomainNode()


class DomainNode(template.Node):
    def render(self, context):
        context['domain'] = Site.objects.get_current().domain[:-1]
        return ''

register = template.Library()
register.tag('get_domain', do_domain)
