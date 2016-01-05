import re

from django.core.urlresolvers import reverse
from django.core.files.base import ContentFile

from django_webtest import WebTest

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
            str(Artist),
            href=reverse('artist-detail', kwargs={'slug': Artist.slug})
        )

    def test_invisible(self):
        Artist = ArtistFactory.create(visible=False)
        artist_list = self.app.get(
            reverse('artist-list')
        )
        assert str(Artist) not in artist_list


class ArtistDetailTest(WebTest):

    def test_visible_exists(self):
        Artist = ArtistFactory.create()
        artist_detail = self.app.get(Artist.get_absolute_url())
        self.assertIn(str(Artist), artist_detail)

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
        Artist = ArtistFactory.create(resume="")
        artist_detail = self.app.get(Artist.get_absolute_url())

        with self.assertRaises(IndexError):
            artist_detail.click(
                'Resume',
                href=reverse('artist-resume', kwargs={'slug': Artist.slug})
            )

    def test_resume_page_link(self):
        Artist = ArtistFactory.create(resume='resume')
        artist_detail = self.app.get(Artist.get_absolute_url())
        artist_detail.click(
            'Resume',
            href=re.escape(Artist.get_resume_url())
        )

    def test_resume_file_link(self):
        Artist = ArtistFactory.create()
        Artist.resume_file.save('file.txt', ContentFile("my string content"))
        artist_detail = self.app.get(Artist.get_absolute_url())
        artist_detail.click(
            'Resume',
            href=re.escape(Artist.get_resume_url())
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
                href=reverse('artist-book-list', kwargs={'slug': Artist.slug})
            )

    def test_book_link(self):
        Artist = ArtistFactory.create(books__n=1)
        artist_detail = self.app.get(Artist.get_absolute_url())

        artist_detail.click(
            'Books',
            href=reverse('artist-book-list', kwargs={'slug': Artist.slug})
        )

    def test_no_website_link(self):
        Artist = ArtistFactory.create(website='')
        artist_detail = self.app.get(Artist.get_absolute_url())

        with self.assertRaises(IndexError):
            artist_detail.click(
                'Website',
            )

    def test_website_link(self):
        Artist = ArtistFactory.create(website='http://test.com/')
        artist_detail = self.app.get(Artist.get_absolute_url())

        artist_detail.click(
            'Website',
            href=re.escape('http://test.com/')
        )


class ArtistPressListTest(WebTest):
    def test_parent_link(self):
        Artist = ArtistFactory.create()
        artist_press_list = self.app.get(
            reverse('artist-press-list', kwargs={'slug': Artist.slug})
        )

        artist_press_list.click(
            str(Artist),
            href=Artist.get_absolute_url()
        )

    def test_detail_link(self):
        Press = PressFactory.create(content='_')
        Artist = ArtistFactory.create(press=Press)
        artist_press_list = self.app.get(
            reverse('artist-press-list', kwargs={'slug': Artist.slug})
        )

        artist_press_list.click(
            str(Press),
            href=reverse('press-detail', kwargs={'slug': Press.slug})
        )


class ArtistExhibitionListTest(WebTest):
    def test_parent_link(self):
        Artist = ArtistFactory.create()
        artist_exhibition_list = self.app.get(
            reverse('artist-exhibition-list', kwargs={'slug': Artist.slug})
        )
        artist_exhibition_list.click(
            str(Artist),
            href=Artist.get_absolute_url()
        )

    def test_detail_link(self):
        Artist = ArtistFactory.create(exhibitions__n=1)
        Exhibition = Artist.exhibitions.all()[0]
        artist_exhibition_list = self.app.get(
            reverse('artist-exhibition-list', kwargs={'slug': Artist.slug})
        )

        artist_exhibition_list.click(
            str(Exhibition),
            href=reverse('exhibition-detail', kwargs={'slug': Exhibition.slug})
        )


class ArtistResumeTest(WebTest):
    def test_parent_link(self):
        Artist = ArtistFactory.create()
        artist_resume = self.app.get(
            reverse('artist-resume', kwargs={'slug': Artist.slug})
        )
        artist_resume.click(
            str(Artist),
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
            str(Artist),
            href=Artist.get_absolute_url()
        )

    def test_link(self):
        Artist = ArtistFactory.create(books__n=1)
        Book = Artist.books.all()[0]
        artist_book_list = self.app.get(
            reverse('artist-book-list', kwargs={'slug': Artist.slug})
        )

        artist_book_list.click(
            Book.title,
            href=Book.get_absolute_url(),
        )
