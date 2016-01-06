from django.test import TestCase

from .factories import ExhibitionFactory


class ExhibitionPressReleasePhotoTest(TestCase):
    def test_no_photo(self):
        Exhibition = ExhibitionFactory(press_release_photo=None)
        assert not Exhibition.get_press_release_photo()

    def test_uploaded_photo(self):
        Exhibition = ExhibitionFactory.create()

        assert Exhibition.get_press_release_photo()['url'] == Exhibition.press_release_photo.url

    def test_related_photo(self):
        Exhibition = ExhibitionFactory.create(photos__n=1, press_release_photo=None)

        assert Exhibition.get_press_release_photo() == Exhibition.photos.all()[0].safe_thumbnail_image

    def test_uploaded_overrides_related_photo(self):
        Exhibition = ExhibitionFactory.create(photos__n=1)

        assert Exhibition.get_press_release_photo()['url'] == Exhibition.press_release_photo.url


class ExhibitionNotGroupShowTest(TestCase):
    def test_no_artists(self):
        Exhibition = ExhibitionFactory(artists__n=0)
        assert not Exhibition.not_group_show

    def test_one_artist(self):
        Exhibition = ExhibitionFactory(artists__n=1)
        assert Exhibition.not_group_show

    def test_two_artists(self):
        Exhibition = ExhibitionFactory(artists__n=2)
        assert Exhibition.not_group_show

    def test_three_or_more_artists(self):
        Exhibition = ExhibitionFactory(artists__n=3)
        assert not Exhibition.not_group_show


class ExhibitionJoinArtistsTest(TestCase):
    def test_no_artists(self):
        Exhibition = ExhibitionFactory(artists__n=0)
        assert Exhibition.join_artists == ''

    def test_one_artist(self):
        Exhibition = ExhibitionFactory(artists__n=1)

        assert Exhibition.join_artists == '{}'.format(str(Exhibition.artists.all()[0]))

    def test_two_artists(self):
        Exhibition = ExhibitionFactory(artists__n=2)

        assert Exhibition.join_artists == '{} and {}'.format(
            str(Exhibition.artists.all()[0]),
            str(Exhibition.artists.all()[1])
        )

    def test_three_or_more_artists(self):
        Exhibition = ExhibitionFactory(artists__n=3)

        assert Exhibition.join_artists == '{}, {}, and {}'.format(
            str(Exhibition.artists.all()[0]),
            str(Exhibition.artists.all()[1]),
            str(Exhibition.artists.all()[2])
        )
