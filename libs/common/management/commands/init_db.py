import os
from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.core.management import call_command


class Command(NoArgsCommand):
    help = 'Add initial data to blank datavase'
    option_list = NoArgsCommand.option_list + (
        make_option(
            '--init',
            action='store_true',
            dest='init',
            default=False,
            help='Tells Django to add factory models'
        ),
    )

    def handle(self, *args, **options):
        self.log('Adding cache table')
        call_command('createcachetable', 'cache', interactive=False, verbosity=0)
        self.log('Initial sync')
        call_command('syncdb', interactive=False, verbosity=0)
        self.log('Initial migrate')
        call_command('migrate', interactive=False, verbosity=0)
        self.log('Adding super user')
        call_command(
            'create_user_permissions',
            os.environ['ADMIN_USERNAME'],
            os.environ['ADMIN_PASSWORD'],
            'admin',
            'contenttypes',
            'url_tracker',
            'sessions',
            'auth'
        )
        call_command('set_site')
        self.log('Loading contact fixture')
        call_command('loaddata', 'configs/fixtures/contact.json')
        if options.get('init'):
            self.log('Adding test_data')
            call_command('test_data')

    def log(self, string):
        self.stdout.write(string + '\n')
