from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Clone one bucket to another'
    args = '(<source bucket name>, <destination bucket name>)'

    def handle(self, *args, **options):
        SOURCE_BUCKET_NAME = args[0]
        DESTINATION_BUCKET_NAME = args[1]
        if DESTINATION_BUCKET_NAME == SOURCE_BUCKET_NAME:
            return
        connection = default_storage.connection
        source_bucket = connection.get_bucket(SOURCE_BUCKET_NAME)
        destination_bucket = connection.get_bucket(DESTINATION_BUCKET_NAME)
        destination_bucket.delete_keys(destination_bucket.list())
        for key in source_bucket.list():
            key.copy(DESTINATION_BUCKET_NAME, key.name)
