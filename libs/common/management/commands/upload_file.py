from boto.s3.key import Key

from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Add a file to the bucket, print url of object'
    args = '<file_name>'

    def handle(self, *args, **options):
        file_name = args[0]
        connection = default_storage.connection
        bucket = connection.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        key = Key(bucket)
        key.key = file_name
        key.set_contents_from_filename(file_name)
        print(key.generate_url(60 * 60))
