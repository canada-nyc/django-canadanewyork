import StringIO
from datetime import date
import random

from PIL import Image
from factory.fuzzy import BaseFuzzyAttribute

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
from django.core.management import call_command
from django.db.models import loading


def django_image(name, size=200, color='red', width=None, height=None):
    if width and height:
        dimensions = (width, height)
    else:
        dimensions = (size, size)

    thumb = Image.new('RGB', dimensions, color)

    thumb_io = StringIO.StringIO()
    thumb.save(thumb_io, format='JPEG')
    thumb_io.seek(0)

    return InMemoryUploadedFile(thumb_io, None, name, 'image/jpeg', thumb_io.len, None)


class AddAppMixin(object):
    custom_apps = ()

    def _pre_setup(self):
        # Add the models to the db.
        self._original_installed_apps = list(settings.INSTALLED_APPS)
        settings.INSTALLED_APPS += self.custom_apps
        loading.cache.loaded = False
        call_command('syncdb', interactive=False, verbosity=0, migrate=False)
        # Call the original method that does the fixtures etc.
        super(AddAppMixin, self)._pre_setup()

    def _post_teardown(self):
        # Call the original method.
        super(AddAppMixin, self)._post_teardown()
        # Restore the settings.
        settings.INSTALLED_APPS = self._original_installed_apps
        loading.cache.loaded = False


def random_date(start_date=date(2005, 1, 1), end_date=date.today()):
    return date.fromordinal(random.randint(start_date.toordinal(), end_date.toordinal()))


class FuzzyDate(BaseFuzzyAttribute):
    def __init__(self, start_date=date(2005, 1, 1), end_date=date.today(), **kwargs):
        super(FuzzyDate, self).__init__(**kwargs)
        self.start_date = start_date.toordinal()
        self.end_date = end_date.toordinal()

    def fuzz(self):
        return date.fromordinal(random.randint(self.start_date, self.end_date))
