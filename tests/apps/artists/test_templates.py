from django_webtest import WebTest
from django.core.urlresolvers import reverse

from .factories import ArtistFactory
from ..press.factories import PressFactory
from ..exhibitions.factories import ExhibitionFactory


class ArtistListTest(WebTest):
    def test_reverse(self):
        self.app.get(
            reverse('artist-list')
        )

    def test_nav_click(self):
        artist_list = self.app.get(
            reverse('artist-list')
        )
        artist_list.click(
            'Artists',
            reverse('artist-list')
        )

    def test_visible(self):
        Artist = ArtistFactory.create()
        artist_list = self.app.get(
            reverse('artist-list')
        )

        artist_list.click(
            unicode(Artist),
            reverse('artist-detail', kwargs={'slug': Artist.slug})
        )

    def test_invisible(self):
        Artist = ArtistFactory.create(visible=False)
        artist_list = self.app.get(
            reverse('artist-list')
        )
        assert unicode(Artist) not in artist_list


class ArtistDetailTest(WebTest):
    def test_visible_exists(self):
        Artist = ArtistFactory.create()
        artist_detail = self.app.get(Artist.get_absolute_url())
        self.assertIn(unicode(Artist), artist_detail)

    def test_invisible_doesnt_exist(self):
        Artist = ArtistFactory.create(visible=False)
        self.app.get(Artist.get_absolute_url(), status=404)

    def test_no_exhibitions_link(self):
        Artist = ArtistFactory.create()
        artist_detail = self.app.get(Artist.get_absolute_url())
        with self.assertRaises(IndexError):
            artist_detail.click('Exhibitions')

    def test_exhibitions_link(self):
        Artist = ArtistFactory.create(exhibitions__n=1)
        artist_detail = self.app.get(Artist.get_absolute_url())
        artist_detail.click(
            'Exhibitions',
            href=reverse('artist-exhibition-list', kwargs={'slug': Artist.slug})
        )

    def test_no_resume_link(self):
        Artist = ArtistFactory.create()
        artist_detail = self.app.get(Artist.get_absolute_url())

        with self.assertRaises(IndexError):
            artist_detail.click('Resume')

    def test_resume_link(self):
        Artist = ArtistFactory.create(resume='resume')
        artist_detail = self.app.get(Artist.get_absolute_url())

        artist_detail.click(
            'Resume',
            href=reverse('artist-resume', kwargs={'slug': Artist.slug})
        )

    def test_no_press_link(self):
        Artist = ArtistFactory.create()
        artist_detail = self.app.get(Artist.get_absolute_url())
        with self.assertRaises(IndexError):
            artist_detail.click('Press')

    def test_press_link(self):
        Artist = ArtistFactory.create(press__n=1)
        artist_detail = self.app.get(Artist.get_absolute_url())

        artist_detail.click(
            'Press',
            href=reverse('artist-press-list', kwargs={'slug': Artist.slug})
        )


class ArtistPressListTest(WebTest):
    def test_parent_link(self):
        Artist = ArtistFactory.create()
        artist_press_list = self.app.get(
            reverse('artist-press-list', kwargs={'slug': Artist.slug})
        )

        artist_press_list.click(
            unicode(Artist),
            href=Artist.get_absolute_url()
        )

    def test_detail_link(self):
        Press = PressFactory.create()
        Artist = ArtistFactory.create(press=Press)
        artist_press_list = self.app.get(
            reverse('artist-press-list', kwargs={'slug': Artist.slug})
        )

        artist_press_list.click(
            unicode(Press),
            reverse('press-detail', kwargs={'slug': Press.slug})
        )

    def test_empty(self):
        Artist = ArtistFactory.create()
        artist_press_list = self.app.get(
            reverse('artist-press-list', kwargs={'slug': Artist.slug})
        )
        self.assertIn('no', artist_press_list)


class ArtistExhibitionListTest(WebTest):
    def test_parent_link(self):
        Artist = ArtistFactory.create()
        artist_exhibition_list = self.app.get(
            reverse('artist-exhibition-list', kwargs={'slug': Artist.slug})
        )
        artist_exhibition_list.click(
            unicode(Artist),
            href=Artist.get_absolute_url()
        )

    def test_detail_link(self):
        Exhibition = ExhibitionFactory.create()
        Artist = ArtistFactory.create(exhibitions=Exhibition)
        artist_exhibition_list = self.app.get(
            reverse('artist-exhibition-list', kwargs={'slug': Artist.slug})
        )

        artist_exhibition_list.click(
            unicode(Exhibition),
            reverse('exhibition-detail', slug=Exhibition.slug)
        )

    def test_empty(self):
        Artist = ArtistFactory.create()
        artist_exhibition_list = self.app.get(
            reverse('artist-exhibition-list', kwargs={'slug': Artist.slug})
        )
        self.assertIn('no', artist_exhibition_list)


class ArtistResumeTest(WebTest):
    def test_parent_link(self):
        Artist = ArtistFactory.create()
        artist_resume = self.app.get(
            reverse('artist-resume', kwargs={'slug': Artist.slug})
        )
        artist_resume.click(
            unicode(Artist),
            href=Artist.get_absolute_url()
        )

    def test_content(self):
        Artist = ArtistFactory.create(resume='theres a resume')
        artist_resume = self.app.get(
            reverse('artist-resume', kwargs={'slug': Artist.slug})
        )
        self.assertIn(Artist.resume, artist_resume)

    def test_empty(self):
        Artist = ArtistFactory.create()
        artist_resume = self.app.get(
            reverse('artist-resume', kwargs={'slug': Artist.slug})
        )
        self.assertIn('no', artist_resume)
