import os

from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Add initial data to blank database'

    def add_arguments(self, parser):
        parser.add_argument('site', help='domain for the site')

        parser.add_argument(
            '--init',
            action='store_true',
            dest='init',
            default=False,
            help='Tells Django to add factory models')

    def handle(self, *args, **options):
        self.log('Adding cache table')
        try:
            call_command('createcachetable', 'cache', interactive=False, verbosity=0)
        except CommandError:
            self.log('Table already created')
        self.log('Initial migrate')
        call_command('migrate', interactive=False, verbosity=0)
        self.log('Adding super user')
        call_command(
            'create_super_user',
            os.environ['ADMIN_USERNAME'],
            os.environ['ADMIN_PASSWORD'])
        self.log('Setting site to ' + options['site'])
        self.set_site(options['site'])

        if options['init']:
            self.log('Adding test_data')
            call_command('test_data')

    def set_site(self, domain):
        site = Site.objects.get_current()
        site.domain = site.name = domain
        site.save()

    def log(self, string):
        self.stdout.write(string + '\n')
