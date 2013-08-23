from django.test import TestCase

from .factories import ExhibitionFactory


class ExhibitionPressReleasePhotoTest(TestCase):
    def test_no_photo(self):
        Exhibition = ExhibitionFactory()
        self.assertFalse(Exhibition.get_press_release_photo())

    def test_uploaded_photo(self):
        Exhibition = ExhibitionFactory.create(press_release_photo__make=True)

        self.assertEqual(Exhibition.get_press_release_photo()['url'], Exhibition.press_release_photo.url)

    def test_related_photo(self):
        Exhibition = ExhibitionFactory.create(photos__n=1)

        self.assertEqual(Exhibition.get_press_release_photo(), Exhibition.photos.all()[0].safe_thumbnail_image)

    def test_uploaded_overrides_related_photo(self):
        Exhibition = ExhibitionFactory.create(photos__n=1, press_release_photo__make=True)

        self.assertEqual(Exhibition.get_press_release_photo()['url'], Exhibition.press_release_photo.url)
