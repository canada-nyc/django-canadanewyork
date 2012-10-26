from django.test import TestCase
from django.core.management import call_command
from django.db.models import loading
from django.test.utils import override_settings
from django.conf import settings
from django.template.defaultfilters import slugify

from .factories import SlugModelFactory


@override_settings(INSTALLED_APPS=settings.INSTALLED_APPS + ('tests.apps.slugify',))
class TestContentRedirects(TestCase):
    def setUp(self):
        loading.cache.loaded = False
        call_command('syncdb', interactive=False)

    def test_save(self):
        _SlugModel = SlugModelFactory()
        #import ipdb;ipdb.set_trace()
        calculated_slug = slugify('-'.join([_SlugModel.text, str(_SlugModel.related_model)]))
        model_slug = _SlugModel.slug
        self.assertEqual(calculated_slug, model_slug)
        _SlugModel.text = 'new_text'
        _SlugModel.save()
        self.assertEqual(calculated_slug, model_slug)