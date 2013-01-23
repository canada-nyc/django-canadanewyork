from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Set domain on site framework'
    args = '(<domain (canada-development.herokuapps.com)>)'

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError('Called with one argument, specifiying the domain of the site')
        site = Site.objects.get_current()
        print 'Settings site to {}'.format(args[0])
        site.domain = site.name = args[0]
        site.save()
