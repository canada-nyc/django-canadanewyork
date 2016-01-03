import os
from optparse import make_option

from django.core.management.base import NoArgsCommand, CommandError
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
        call_command('set_site')
        if options.get('init'):
            self.log('Adding test_data')
            call_command('test_data')

    def log(self, string):
        self.stdout.write(string + '\n')
