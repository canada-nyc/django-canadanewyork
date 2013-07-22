import re

from django_webtest import WebTest
from django.core.urlresolvers import reverse
from webtest.app import AppError

from .factories import ArtistFactory
from ..press.factories import PressFactory


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
            href=reverse('artist-list')
        )

    def test_visible(self):
        Artist = ArtistFactory.create()
        artist_list = self.app.get(
            reverse('artist-list')
        )

        artist_list.click(
            unicode(Artist),
            href=reverse('artist-detail', kwargs={'slug': Artist.slug})
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
            artist_detail.click(
                'Exhibitions',
                href=reverse('artist-exhibition-list', kwargs={'slug': Artist.slug})
            )

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
            artist_detail.click(
                'Resume',
                href=reverse('artist-resume', kwargs={'slug': Artist.slug})
            )

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
            artist_detail.click(
                'Press',
                href=reverse('artist-press-list', kwargs={'slug': Artist.slug})
            )

    def test_press_link(self):
        Artist = ArtistFactory.create(press__n=1)
        artist_detail = self.app.get(Artist.get_absolute_url())

        artist_detail.click(
            'Press',
            href=reverse('artist-press-list', kwargs={'slug': Artist.slug})
        )

    def test_no_book_link(self):
        Artist = ArtistFactory.create()
        artist_detail = self.app.get(Artist.get_absolute_url())
        with self.assertRaises(IndexError):
            artist_detail.click(
                'Books',
            )

    def test_book_link(self):
        Artist = ArtistFactory.create(books__n=1)
        artist_detail = self.app.get(Artist.get_absolute_url())

        artist_detail.click(
            'Books',
            href=reverse('artist-book-list', kwargs={'slug': Artist.slug})
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
        Press = PressFactory.create(content='_')
        Artist = ArtistFactory.create(press=Press)
        artist_press_list = self.app.get(
            reverse('artist-press-list', kwargs={'slug': Artist.slug})
        )

        artist_press_list.click(
            unicode(Press),
            href=reverse('press-detail', kwargs={'slug': Press.slug})
        )


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
        Artist = ArtistFactory.create(exhibitions__n=1)
        Exhibition = Artist.exhibitions.all()[0]
        artist_exhibition_list = self.app.get(
            reverse('artist-exhibition-list', kwargs={'slug': Artist.slug})
        )

        artist_exhibition_list.click(
            unicode(Exhibition),
            href=reverse('exhibition-detail', kwargs={'slug': Exhibition.slug})
        )


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


class ArtistBookListTest(WebTest):
    def test_parent_link(self):
        Artist = ArtistFactory.create()
        artist_book_list = self.app.get(
            reverse('artist-book-list', kwargs={'slug': Artist.slug})
        )

        artist_book_list.click(
            unicode(Artist),
            href=Artist.get_absolute_url()
        )

    def test_email_link(self):
        Artist = ArtistFactory.create(books__n=1)
        Book = Artist.books.all()[0]
        artist_book_list = self.app.get(
            reverse('artist-book-list', kwargs={'slug': Artist.slug})
        )

        # will raise AppError when hits 404, because index link is not a real
        # page, but a mailto link
        with self.assertRaises(AppError):
            artist_book_list.click(
                unicode(Book),
                href=re.escape(Book.get_purchase_url()),
            )
