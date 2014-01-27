from decimal import Decimal as D

from django.test import TestCase

from simpleimages.utils import perform_transformation

from apps.photos.models import ArtworkPhoto
from ...utils import AddAppMixin, django_image
from .factories import MockPhotoFactory


class ArtworkPhotoDimensionTest(TestCase):
    def setUp(self):
        self.photo = ArtworkPhoto()

    def test_dimensions(self):
        self.photo.height = 10
        self.photo.width = 10
        self.photo.depth = None

        self.assertItemsEqual(self.photo.dimensions, [10, 10])

    def test_convert_inches_to_cm(self):
        cm = self.photo.convert_inches_to_cm(1)

        self.assertEqual(cm, D('2.54'))

    def test_dimensions_cm(self):
        self.photo.height = 1

        self.assertEqual(self.photo.dimensions_cm, [D('2.54')])

    def test_full_dimensions(self):
        self.photo.height = .5
        self.photo.width = .5

        self.assertEqual(
            self.photo.full_dimensions,
            '1/2 x 1/2 in (1.27 x 1.27 cm)'
        )

    def test_full_dimensions_single(self):
        self.photo.height = 1

        self.assertEqual(
            self.photo.full_dimensions,
            '1 in (2.54 cm)'
        )

    def test_full_dimensions_double_digit(self):
        self.photo.height = 10

        self.assertEqual(
            self.photo.full_dimensions,
            '10 in (25.4 cm)'
        )


class ArtworkPhotoCachedDimensionsTest(AddAppMixin, TestCase):
    custom_apps = ('tests.apps.photos',)

    def test_dimension_fields_filled(self):
        photo = MockPhotoFactory(image__size=1000)
        self.assertTrue(photo.thumbnail_image)
        self.assertEqual(photo.thumbnail_image.height, photo.thumbnail_image_height)

    def test_dimensions_field_change(self):
        photo = MockPhotoFactory(image__size=10)
        self.assertEqual(photo.thumbnail_image.height, photo.thumbnail_image_height, 10)

        photo.image.save('_.jpg', django_image('_.jpg', size=1000))
        self.assertEqual(photo.thumbnail_image.height, photo.thumbnail_image_height)
        self.assertNotEqual(photo.thumbnail_image.height, 10)

    def test_overriding_existing(self):
        photo = MockPhotoFactory(image__size=10)
        photo.thumbnail_image_height = 1000
        photo.save(update_fields=['thumbnail_image_height'])
        self.assertEqual(photo.thumbnail_image_height, 1000)

        perform_transformation(photo)

        self.assertNotEqual(photo.thumbnail_image_height, 1000)


class ArtworkPhotoFullCaptionTest(TestCase):
    def setUp(self):
        self.photo = ArtworkPhoto()

    def test_dimensions(self):
        self.photo.height = 1

        self.assertIn(
            self.photo.full_dimensions,
            self.photo.full_caption
        )
