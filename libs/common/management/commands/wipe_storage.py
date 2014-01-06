from subprocess import call
from optparse import make_option

from django.core.management.base import NoArgsCommand
from django.conf import settings
from django.core.files.storage import default_storage


class Command(NoArgsCommand):
    help = 'Wipes either local or S3 static and media storage'

    option_list = NoArgsCommand.option_list + (
        make_option(
            '--only_static',
            action='store_true',
            dest='only_static',
            default=False,
            help='Only wipe static and not media'
        ),
    )

    def handle(self, *args, **options):
        if settings.DEFAULT_FILE_STORAGE != 'django.core.files.storage.FileSystemStorage':
            self.log(
                'Found bucket {}'.format(settings.AWS_STORAGE_BUCKET_NAME))
            self.log('Getting connection...')
            connection = default_storage.connection
            self.log('Getting bucket...')
            bucket = connection.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
            self.log('Deleting keys in bucket...')
            bucket.delete_keys(bucket.list())
        else:
            self.log('Found local storage')
            if not options.get('only_static'):
                self.log('Deleting {}'.format(settings.MEDIA_ROOT))
                call('rm -rf {}'.format(settings.MEDIA_ROOT), shell=True)
            self.log('Deleting {}'.format(settings.STATIC_ROOT))
            call('rm -rf {}'.format(settings.STATIC_ROOT), shell=True)

    def log(self, string):
        self.stdout.write(string + '\n')
