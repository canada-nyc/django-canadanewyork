from django.conf import settings

from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = 'prints the database name'
    requires_model_validation = False

    def handle(self, *args, **options):
        self.stdout.write(settings.DATABASES['default']['NAME'], ending='')
