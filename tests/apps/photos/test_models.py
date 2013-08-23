from decimal import Decimal as D

from django.test import TestCase

from apps.photos.models import ArtworkPhoto


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


class ArtworkPhotoFullCaptionTest(TestCase):
    def setUp(self):
        self.photo = ArtworkPhoto()

    def test_dimensions(self):
        self.photo.height = 1

        self.assertIn(
            self.photo.full_dimensions,
            self.photo.full_caption
        )
