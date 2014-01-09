from django.core.management.base import NoArgsCommand, CommandError
from django.conf import settings
from django.core.files.storage import default_storage


class Command(NoArgsCommand):
    help = 'Deletes the canada static folder on S3'

    def handle(self, *args, **options):
        prefix = 'canada/'
        try:
            self.log(
                '    Found bucket {}'.format(settings.AWS_STORAGE_BUCKET_NAME))
        except AttributeError:
            raise CommandError('Must be using S3 to delete only static')
        self.log('    Getting connection...')
        connection = default_storage.connection
        self.log('    Getting bucket...')
        bucket = connection.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        keys = list(bucket.list(prefix=prefix))
        self.log('    Found {} keys in path "{}"...'.format(len(keys), prefix))
        self.log('    Deleting keys...')
        bucket.delete_keys(keys)

    def log(self, string):
        self.stdout.write(string + '\n')
