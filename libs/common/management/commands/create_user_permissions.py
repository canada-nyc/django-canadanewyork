from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission


class Command(BaseCommand):
    args = '<username> <password> [<app_name app_name ...>]'
    help = ('Creates staff user and adds all permissions except those in the'
            'app(s) specified')

    def handle(self, *args, **options):
        username, password = args[:2]
        excluded_app_labels = args[2:]
        self.stdout.write("Creating User {}:{}".format(username, password))
        user = User(username=username, is_staff=True)
        user.set_password(password)
        user.save()
        self.stdout.write("Adding permissions for all apps but {}".format(
            str(excluded_app_labels)
        ))
        user.user_permissions = Permission.objects.exclude(
            content_type__app_label__in=excluded_app_labels
        )
        user.save()
