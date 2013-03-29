from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Removes a key from the S3 bucket'
    args = '<file_name>'

    def handle(self, *args, **options):
        file_name = args[0]
        connection = default_storage.connection
        bucket = connection.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        key = bucket.get_key(file_name)
        assert key
        key.delete()
