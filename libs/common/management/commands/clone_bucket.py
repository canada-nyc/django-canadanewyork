from __future__ import print_function

from concurrent import futures

from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Clone one bucket to another'
    args = '(<source bucket name>, <destination bucket name>)'

    def handle(self, *args, **options):
        SOURCE_BUCKET_NAME = args[0]
        DESTINATION_BUCKET_NAME = args[1]
        if DESTINATION_BUCKET_NAME == SOURCE_BUCKET_NAME:
            return

        self.log('Copying {} -> {}'.format(
            SOURCE_BUCKET_NAME,
            DESTINATION_BUCKET_NAME)
        )
        self.log('Getting connection')
        connection = default_storage.connection
        self.log('Getting source bucket')
        source_bucket = connection.get_bucket(SOURCE_BUCKET_NAME)
        self.log('Getting destination bucket')
        destination_bucket = connection.get_bucket(DESTINATION_BUCKET_NAME)

        self.log('Deleting keys')
        destination_bucket.delete_keys(destination_bucket.list())
        self.log('Copying new keys')

        def copy_key(key):
            key.copy(DESTINATION_BUCKET_NAME, key.name, preserve_acl=True)
            print(key.name)

        with futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_key = {executor.submit(copy_key, key): key for key in source_bucket.list()}
            for future in futures.as_completed(future_to_key):
                key = future_to_key[future]
                try:
                    future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (key, exc))

        self.log('Getting CORS')
        cors_cfg = source_bucket.get_cors()
        self.log('Deleting old CORS')
        destination_bucket.delete_cors()
        self.log('Setting new CORS')
        destination_bucket.set_cors(cors_cfg)

    def log(self, message):
        print('{}...'.format(message))
