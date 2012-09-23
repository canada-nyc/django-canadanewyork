from optparse import make_option
from subprocess import call

from django.core.management.base import NoArgsCommand
from django.core.management import call_command


class Command(NoArgsCommand):
    help = 'Wipes DB and static and reinstalls with default data'
    option_list = NoArgsCommand.option_list + (
        make_option('--no-wipe', dest='wipe', default=True, action='store_false',
            help='Don\'t remove ./static/ and sqlite.db'),
        )

    def handle(self, *args, **options):
        if options.get('wipe'):
                self.stdout.write('Removing sqlite.db\n')
                call('rm -f sqlite.db', shell=True)
                self.stdout.write('Removing ./static\n')
                call('rm -rf static', shell=True)

        self.log('Syncing DB')
        call_command('syncdb', interactive=False, verbosity=0)
        self.log('Migrating DB')
        call_command('migrate', verbosity=0)
        self.log('Collecting Static DB')
        call_command('collectstatic', interactive=False, verbosity=0)
        self.log('Adding SU')
        call_command('add_superuser')
        self.log('Adding test_data')
        call_command('test_data')

    def log(self, string):
        self.stdout.write(string + '\n')
