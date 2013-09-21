from django.db import connection, transaction

from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    help = 'Wipes `cache` database table'

    def handle(self, *args, **options):
        cursor = connection.cursor()

        cursor.execute("DELETE FROM cache")
        transaction.commit_unless_managed()
