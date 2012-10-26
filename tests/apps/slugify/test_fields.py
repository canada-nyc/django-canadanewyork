from django.test import TestCase
from django.core.management import call_command
from django.db.models import loading
from django.test.utils import override_settings
from django.conf import settings
from django.template.defaultfilters import slugify

from .factories import SlugifyModelFactory, SlugifyDateModelFactory


@override_settings(INSTALLED_APPS=settings.INSTALLED_APPS + ('tests.apps.slugify',))
class TestContentRedirects(TestCase):
    def setUp(self):
        loading.cache.loaded = False
        call_command('syncdb', interactive=False)

    def test_save(self):
        _SlugifyModel = SlugifyModelFactory()
        calculated_slug = slugify('-'.join([_SlugifyModel.text, str(_SlugifyModel.related_model)]))
        model_slug = _SlugifyModel.slug
        self.assertEqual(calculated_slug, model_slug)

    def test_no_change_on_save(self):
        _SlugifyModel = SlugifyModelFactory()
        calculated_slug = slugify('-'.join([_SlugifyModel.text, str(_SlugifyModel.related_model)]))
        _SlugifyModel.text = 'new_text'
        _SlugifyModel.save()
        model_slug = _SlugifyModel.slug
        self.assertEqual(calculated_slug, model_slug)

    def test_lambda(self):
        _SlugifyDateModel = SlugifyDateModelFactory()
        calculated_slug = slugify('-'.join([_SlugifyDateModel.text, str(_SlugifyDateModel.date.year)]))
        model_slug = _SlugifyDateModel.slug
        self.assertEqual(calculated_slug, model_slug)
