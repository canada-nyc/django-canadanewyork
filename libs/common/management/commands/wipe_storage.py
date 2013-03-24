from subprocess import call

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.core.files.storage import default_storage


class Command(NoArgsCommand):
    help = 'Wipes either local or S3 static and media storage'

    def handle(self, *args, **options):
        self.log('Wiping storage')
        self.log('    Found bucket {}'.format(settings.AWS_STORAGE_BUCKET_NAME))
        self.log('    Getting connection...')
        connection = default_storage.connection
        self.log('    Getting bucket...')
        bucket = connection.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)

        self.log('    Deleting keys in bucket...')
        bucket.delete_keys(bucket.list())

    def log(self, string):
        self.stdout.write(string + '\n')
