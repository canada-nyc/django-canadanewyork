from subprocess import call

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.core.files.storage import default_storage


class Command(NoArgsCommand):
    help = 'Wipes either local or S3 static and media storage'

    def handle(self, *args, **options):
        if settings.DEFAULT_FILE_STORAGE != 'django.core.files.storage.FileSystemStorage':
            self.log('    Found bucket {}'.format(settings.AWS_STORAGE_BUCKET_NAME))
            self.log('    Getting connection...')
            connection = default_storage.connection
            self.log('    Getting bucket...')
            bucket = connection.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
            self.log('    Deleting keys in bucket...')
            bucket.delete_keys(bucket.list())
        else:
            self.log('    Found local storage')
            self.log('        Deleting')
            self.log('            {}'.format(settings.MEDIA_ROOT))
            call('rm -rf {}'.format(settings.MEDIA_ROOT), shell=True)
            self.log('            {}'.format(settings.STATIC_ROOT))
            call('rm -rf {}'.format(settings.STATIC_ROOT), shell=True)

    def log(self, string):
        self.stdout.write(string + '\n')
