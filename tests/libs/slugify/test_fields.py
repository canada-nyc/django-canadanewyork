from django.test import TestCase
from django.template.defaultfilters import slugify
from django.db import IntegrityError

from . import models as slug_models
from ...utils import AddAppMixin


class TestSlugify(AddAppMixin, TestCase):
    custom_apps = ('tests.libs.slugify',)

    def test_save(self):
        _SlugifyModel = slug_models.SlugifyModel.objects.create(
            text='text',
            related_model=slug_models.RelatedModel.objects.create()
        )
        calculated_slug = slugify('-'.join([_SlugifyModel.text, str(_SlugifyModel.related_model)]))
        model_slug = _SlugifyModel.slug
        self.assertEqual(calculated_slug, model_slug)

    def test_change_on_save(self):
        _SlugifyModel = slug_models.SlugifyModel.objects.create(
            text='text',
            related_model=slug_models.RelatedModel.objects.create()
        )
        _SlugifyModel.text = 'new_text'
        _SlugifyModel.save()
        new_calculated_slug = slugify('-'.join([_SlugifyModel.text, str(_SlugifyModel.related_model)]))
        model_slug = _SlugifyModel.slug
        self.assertEqual(new_calculated_slug, model_slug)

    def test_max_length(self):
        _SlugifyModel = slug_models.SlugifyModel.objects.create(
            text='s' * 300,
            related_model=slug_models.RelatedModel.objects.create()
        )
        model_slug = _SlugifyModel.slug
        self.assertLess(len(model_slug), 255)

    def test_unique(self):
        slug_models.SlugifyUniqueModel.objects.create(
            text='text',
        )
        with self.assertRaises(IntegrityError):
            slug_models.SlugifyUniqueModel.objects.create(
                text='text',
            )

    def test_template(self):
        _SlugifyTemplateModel = slug_models.SlugifyTemplateModel.objects.create(
            text='text',
            text2='text2 other'
        )
        calculated_slug = 'text/text2-other'
        model_slug = _SlugifyTemplateModel.slug
        self.assertEqual(calculated_slug, model_slug)

    def test_callable(self):
        _SlugifyPopulateFromCallableModel = slug_models.SlugifyPopulateFromCallableModel.objects.create()
        calculated_slug = unicode(_SlugifyPopulateFromCallableModel)
        model_slug = _SlugifyPopulateFromCallableModel.slug
        self.assertEqual(calculated_slug, model_slug)
