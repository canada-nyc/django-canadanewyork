import os

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.test.utils import override_settings
from django.conf import settings
from django.test import TestCase
from django.db.models import loading


@override_settings(INSTALLED_APPS=settings.INSTALLED_APPS + ('storages',),
                   DEFAULT_FILE_STORAGE='storages.backends.s3boto.S3BotoStorage',
                   AWS_ACCESS_KEY_ID=os.environ.get('AWS_ACCESS_KEY_ID'),
                   AWS_SECRET_ACCESS_KEY=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                   AWS_STORAGE_BUCKET_NAME=os.environ.get('AWS_STORAGE_BUCKET_NAME'),
                   STATICFILES_STORAGE=settings.DEFAULT_FILE_STORAGE)
class S3StorageTest(TestCase):
    def test_storage(self):
        # Standard file access options are available, and work as expected:
        self.assertFalse(default_storage.exists('storage_test'))
        t_file = default_storage.open('storage_test', 'w')
        t_file.write('storage contents')
        t_file.close()

        self.assertTrue(default_storage.exists('storage_test'))
        t_file = default_storage.open('storage_test', 'r')
        self.assertEqual(t_file.read(), 'storage contents')
        t_file.close()

        default_storage.delete('storage_test')
        default_storage.exists('storage_test')
