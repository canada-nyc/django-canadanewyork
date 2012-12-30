from subprocess import call

from boto.s3.connection import S3Connection

from django.core.management.base import NoArgsCommand
from django.conf import settings


class Command(NoArgsCommand):
    help = 'Wipes either local or S3 static and media storage'

    def handle(self, *args, **options):
        self.log('Wiping all storage')
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY and settings.AWS_STORAGE_BUCKET_NAME:
            self.log('    Found bucket {}'.format(settings.AWS_STORAGE_BUCKET_NAME))
            self.log('    Getting connection...')
            connection = S3Connection(
                settings.AWS_ACCESS_KEY_ID,
                settings.AWS_SECRET_ACCESS_KEY
            )
            self.log('    Getting bucket...')
            bucket = connection.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)

            self.log('    Deleting keys in bucket...')
            for key in bucket.list():
                key.delete()
        else:
            self.log('    Found local storage')
            call('rm -rf {}'.format(settings.MEDIA_ROOT), shell=True)
            call('rm -rf {}'.format(settings.STATIC_ROOT), shell=True)

    def log(self, string):
        self.stdout.write(string + '\n')
