from decimal import Decimal as D

from django.test import TestCase
from django.test.utils import override_settings

from simpleimages.utils import perform_transformation

from apps.photos.models import ArtworkPhoto, BasePhoto
from ...utils import AddAppMixin, django_image
from .factories import MockPhotoFactory


class BasePhotoGetSafeImageTest(TestCase):

    def setUp(self):
        self.photo = BasePhoto()
        self.photo.image = lambda _: _
        self.photo.image.url = 'url atrribute'
        self.photo.image.height = 'height atrribute'
        self.photo.image.width = 'width atrribute'
        self.photo.image_height = 'height field'
        self.photo.image_width = 'width field'

        self.photo.backup_image = 'backup image'

        self.get_safe_image = lambda self: self.photo._get_safe_image('image', 'backup_image')

    def test_no_image_returns_backup_image(self):
        self.photo.image = False

        self.assertEqual(
            self.get_safe_image(self),
            'backup image'
        )

    @override_settings(CANADA_IMAGE_DIMENSION_FIELDS='_')
    def test_returns_url(self):
        self.assertEqual(
            self.get_safe_image(self)['url'],
            'url atrribute'
        )

    @override_settings(CANADA_IMAGE_DIMENSION_FIELDS=True)
    def test_returns_dimension_fields(self):
        self.assertEqual(
            self.get_safe_image(self)['width'],
            'width field'
        )

        self.assertEqual(
            self.get_safe_image(self)['height'],
            'height field'
        )

    @override_settings(CANADA_IMAGE_DIMENSION_FIELDS=False)
    def test_no_canada_image_dimension_fields(self):
        self.assertEqual(
            self.get_safe_image(self)['width'],
            'width atrribute'
        )

        self.assertEqual(
            self.get_safe_image(self)['height'],
            'height atrribute'
        )


class BasePhotoCachedDimensionsTest(AddAppMixin, TestCase):
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


class ArtworkPhotoFullCaptionTest(TestCase):
    def setUp(self):
        self.photo = ArtworkPhoto()

    def test_dimensions(self):
        self.photo.height = 1

        self.assertIn(
            self.photo.full_dimensions,
            self.photo.full_caption
        )
