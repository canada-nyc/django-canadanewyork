import pytest

from django.test import TransactionTestCase
from django.template.defaultfilters import slugify
from django.db import IntegrityError

from . import models as slug_models


@slug_models.SlugifyTemplateModel.fake_me
@slug_models.SlugifyUniqueModel.fake_me
@slug_models.SlugifyModel.fake_me
@slug_models.RelatedModel.fake_me
class TestSlugify(TransactionTestCase):
    def test_save(self):
        _SlugifyModel = slug_models.SlugifyModel.objects.create(
            text='text',
            related_model=slug_models.RelatedModel.objects.create()
        )
        calculated_slug = slugify('-'.join([_SlugifyModel.text, str(_SlugifyModel.related_model)]))
        model_slug = _SlugifyModel.slug
        assert calculated_slug == model_slug

    def test_doesnt_change_on_save(self):
        _SlugifyModel = slug_models.SlugifyModel.objects.create(
            text='text',
            related_model=slug_models.RelatedModel.objects.create()
        )
        _SlugifyModel.text = 'new_text'
        _SlugifyModel.save()
        new_calculated_slug = slugify('-'.join(['text', str(_SlugifyModel.related_model)]))
        model_slug = _SlugifyModel.slug
        assert new_calculated_slug == model_slug

    def test_max_length(self):
        _SlugifyModel = slug_models.SlugifyModel.objects.create(
            text='s' * 300,
            related_model=slug_models.RelatedModel.objects.create()
        )
        model_slug = _SlugifyModel.slug
        assert len(model_slug) < 255

    def test_unique(self):
        slug_models.SlugifyUniqueModel.objects.create(
            text='text',
        )
        with pytest.raises(IntegrityError):
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
        assert calculated_slug == model_slug

    def test_available_before_save(self):
        _SlugifyModel = slug_models.SlugifyUniqueModel(
            text='text',
        )
        assert 'text' == _SlugifyModel.slug

    def test_wont_update_before_save(self):
        _SlugifyModel = slug_models.SlugifyUniqueModel.objects.create(
            text='text',
        )
        _SlugifyModel.text = "hey there"
        assert 'text' == _SlugifyModel.slug
