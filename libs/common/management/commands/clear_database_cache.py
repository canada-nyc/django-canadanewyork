from django.core.cache import cache

from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = 'Wipes `cache` database table'

    def handle(self, *args, **options):
        cache.clear()
