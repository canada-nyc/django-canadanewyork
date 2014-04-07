from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    args = '<username> <password>'
    help = ('Creates a super user without user interaction')

    def handle(self, *args, **options):
        username, password = args
        self.stdout.write(
            "Creating super user {}:{}".format(username, password))
        user = User(username=username, is_superuser=True, is_staff=True)
        user.set_password(password)
        user.save()
