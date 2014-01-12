from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site
from django.conf import settings


class Command(BaseCommand):
    help = 'Set domain on site framework. If not provided will use ALLOWED_HOSTS'
    args = '[<domain (canada-development.herokuapps.com)>]'

    def handle(self, *args, **options):
        if not len(args):
            site_name = settings.ALLOWED_HOSTS[0]
        elif len(args) == 1:
            site_name = args[0]
        else:
            raise CommandError('set_site must be called with 0 or 1 arguments')

        if int(options['verbosity']):
            print 'Settings site to {}'.format(site_name)
        site = Site.objects.get_current()
        site.domain = site.name = site_name
        site.save()
