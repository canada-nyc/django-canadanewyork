import os
from optparse import make_option
from subprocess import call

from django.core.management.base import NoArgsCommand
from django.core.management import call_command
from django.contrib.auth.models import User


class Command(NoArgsCommand):
    help = 'Wipes DB and static and reinstalls with default data'
    option_list = NoArgsCommand.option_list + (
        make_option('--no-wipe-db', dest='wipe_db', default=True, action='store_false'),
        make_option('--no-init', dest='init', default=True, action='store_false'),

    )

    def handle(self, *args, **options):
        if options.get('wipe_db'):
                self.stdout.write('Removing static\n')
                call('rm -rf tmp/static', shell=True)
                self.stdout.write('Removing media\n')
                call('rm -rf tmp/media', shell=True)
        self.log('Reseting DB')
        call_command('reset_db', interactive=False, router="default")
        self.log('Initial sync')
        call_command('syncdb', interactive=False, verbosity=0)
        self.log('Initial migrate')
        call_command('migrate', interactive=False, verbosity=0)
        self.log('Collecting Static DB')
        call_command('collectstatic', interactive=False, verbosity=0)
        self.create_superuser(
            os.environ['ADMIN_USERNAME'],
            os.environ['ADMIN_PASSWORD'],
            os.environ['ADMIN_EMAIL'],
        )
        if options.get('init'):
            self.log('Adding test_data')
            call_command('test_data')

    def create_superuser(self, username, password, email):
        self.log('Adding super user')
        call_command('createsuperuser', interactive=False, username=username,
                     email=email)

        self.log('    Setting username: {}'.format(username))
        self.log('    Setting password: {}'.format(password))
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()

    def log(self, string):
        self.stdout.write(string + '\n')
