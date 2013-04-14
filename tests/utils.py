import StringIO

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.core.management import call_command
from django.db.models import loading


def django_image(name, size=10, color='red'):
    thumb = Image.new('RGB', (size, size,), color)

    thumb_io = StringIO.StringIO()
    thumb.save(thumb_io, format='JPEG')
    thumb_io.seek(0)

    return SimpleUploadedFile(name, thumb_io)


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
