from django.test import TestCase

from .factories import ExhibitionFactory


class ExhibitionUnicodeTest(TestCase):
    def test_name(self):
        Exhibition = ExhibitionFactory()
        self.assertEqual(unicode(Exhibition), Exhibition.name)

    def test_one_artist(self):
        Exhibition = ExhibitionFactory(artists__n=1)
        self.assertEqual(unicode(Exhibition), '{}: {}'.format(Exhibition.artists.all()[0], Exhibition.name))

    def test_multiple_artists(self):
        Exhibition = ExhibitionFactory(artists__n=2)
        self.assertEqual(unicode(Exhibition), Exhibition.name)


class ExhibitionPressReleasePhotoTest(TestCase):
    def test_no_photo(self):
        Exhibition = ExhibitionFactory()
        self.assertFalse(Exhibition.get_press_release_photo())

    def test_uploaded_photo(self):
        Exhibition = ExhibitionFactory.create(press_release_photo__make=True)

        self.assertEqual(Exhibition.get_press_release_photo(), Exhibition.press_release_photo)

    def test_related_photo(self):
        Exhibition = ExhibitionFactory.create(photos__n=1)

        self.assertEqual(Exhibition.get_press_release_photo(), Exhibition.photos.all()[0].image)

    def test_uploaded_overrides_related_photo(self):
        Exhibition = ExhibitionFactory.create(photos__n=1, press_release_photo__make=True)

        self.assertEqual(Exhibition.get_press_release_photo(), Exhibition.press_release_photo)


class ExhibitionCurrentManagerTest(TestCase):
    def test_current(self):
        Exhibition = ExhibitionFactory()
        self.assertEqual(Exhibition, Exhibition.__class__.objects.get_current())
