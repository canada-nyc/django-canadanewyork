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


class ExhibitionGroupShowTest(TestCase):
    def test_no_artists(self):
        Exhibition = ExhibitionFactory(artists__n=0)
        self.assertFalse(Exhibition.group_show)

    def test_one_artist(self):
        Exhibition = ExhibitionFactory(artists__n=1)
        self.assertFalse(Exhibition.group_show)

    def test_two_artists(self):
        Exhibition = ExhibitionFactory(artists__n=2)
        self.assertFalse(Exhibition.group_show)

    def test_three_or_more_artists(self):
        Exhibition = ExhibitionFactory(artists__n=3)
        self.assertTrue(Exhibition.group_show)


class ExhibitionJoinArtistsTest(TestCase):
    def test_no_artists(self):
        Exhibition = ExhibitionFactory(artists__n=0)
        self.assertEqual(Exhibition.join_artists, '')

    def test_one_artist(self):
        Exhibition = ExhibitionFactory(artists__n=1)

        self.assertEqual(
            Exhibition.join_artists,
            '{}'.format(unicode(Exhibition.artists.all()[0]))
        )

    def test_two_artists(self):
        Exhibition = ExhibitionFactory(artists__n=2)

        self.assertEqual(
            Exhibition.join_artists,
            '{} and {}'.format(
                unicode(Exhibition.artists.all()[0]),
                unicode(Exhibition.artists.all()[1])
            )
        )

    def test_three_or_more_artists(self):
        Exhibition = ExhibitionFactory(artists__n=3)

        self.assertEqual(
            Exhibition.join_artists,
            '{}, {}, and {}'.format(
                unicode(Exhibition.artists.all()[0]),
                unicode(Exhibition.artists.all()[1]),
                unicode(Exhibition.artists.all()[2])
            )
        )

