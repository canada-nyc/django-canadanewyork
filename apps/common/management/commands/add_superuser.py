from django.contrib.auth.models import User
from django.core import management


class Command(management.base.BaseCommand):
    help = 'Adds default superuser'

    def handle(self, username='saul', password='saul123', *args, **options):
        self.stdout.write('Adding superuser\n')
        admin = User.objects.create_user(username, password)
        admin.is_superuser = True
        admin.save()
        self.stdout.write('    username: {}\n'
                          '    password: {}\n'.format(username, password))
