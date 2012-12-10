from django.test import TestCase
from django.template.defaultfilters import slugify

from .factories import SlugifyModelFactory, SlugifyDateModelFactory
from ...common.base_test import AddAppMixin


class TestContentRedirects(AddAppMixin, TestCase):
    custom_apps = ('tests.libs.slugify',)

    def test_save(self):
        _SlugifyModel = SlugifyModelFactory()
        calculated_slug = slugify('-'.join([_SlugifyModel.text, str(_SlugifyModel.related_model)]))
        model_slug = _SlugifyModel.slug
        self.assertEqual(calculated_slug, model_slug)

    def test_change_on_save(self):
        _SlugifyModel = SlugifyModelFactory()
        _SlugifyModel.text = 'new_text'
        _SlugifyModel.save()
        new_calculated_slug = slugify('-'.join([_SlugifyModel.text, str(_SlugifyModel.related_model)]))
        model_slug = _SlugifyModel.slug
        self.assertEqual(new_calculated_slug, model_slug)

    def test_lambda(self):
        _SlugifyDateModel = SlugifyDateModelFactory()
        calculated_slug = slugify('-'.join([_SlugifyDateModel.text, str(_SlugifyDateModel.date.year)]))
        model_slug = _SlugifyDateModel.slug
        self.assertEqual(calculated_slug, model_slug)
