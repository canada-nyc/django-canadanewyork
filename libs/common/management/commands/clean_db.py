import os
from optparse import make_option

import psycopg2

from django.core.management.base import NoArgsCommand
from django.core.management import call_command
from django.contrib.auth.models import User


class Command(NoArgsCommand):
    help = 'Wipes DB and static and reinstalls with default data'
    option_list = NoArgsCommand.option_list + (
        make_option(
            '--noinput',
            action='store_false',
            dest='interactive',
            default=True,
            help='Tells Django to NOT prompt the user for input of any kind.'
        ),
        make_option(
            '--no-wipe-static',
            action='store_false',
            dest='wipe_static',
            default=True,
            help='Tells Django to NOT wipe static and media locally'
        ),
        make_option(
            '--init',
            action='store_true',
            dest='init',
            default=False,
            help='Tells Django to add factory models'
        ),
    )

    def handle(self, *args, **options):
        self.log('Clearing Cache')
        call_command('clear_cache')
        if options.get('wipe_static'):
            call_command('wipe_storage')
        self.log('Reseting DB')
        try:
            call_command('reset_db', interactive=False, router="default")
        except psycopg2.OperationalError as e:
            if options.get('interactive'):
                if raw_input(
                    ("Error when droppping DB:\n\n {} \n\n Note: if using "
                     "Heroku, have you `heroku pg:reset DATABASE_URL` manually?\n"
                     "(y or yes)\n").format(e)
                ) not in ('yes', 'y'):
                    print 'Do that first'
                    return
            else:
                self.log(
                    ('Assuming db is already wiped\n'
                     '`heroku pg:reset DATABASE_URL` on Heroku')
                )
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
