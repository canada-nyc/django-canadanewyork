import datetime

import pytest

from django.core.urlresolvers import reverse

from django_webtest import WebTest

from .factories import BookFactory


class BookListTest(WebTest):

    def test_reverse(self):
        self.app.get(
            reverse('book-list')
        )

    def test_nav_click_shown(self):
        with self.settings(SHOW_BOOKS=True):
            book_list = self.app.get(
                reverse('book-list')
            )
            book_list.click(
                'Books',
            )

    def test_nav_click_hidden(self):
        with self.settings(SHOW_BOOKS=False):
            book_list = self.app.get(
                reverse('book-list')
            )
            with pytest.raises(IndexError):
                book_list.click(
                    'Books',
                )

    def test_link(self):
        Book = BookFactory.create()
        book_list = self.app.get(
            reverse('book-list')
        )

        book_list.click(
            Book.title,
            href=Book.get_absolute_url()
        ),

    def test_artist(self):
        book = BookFactory.create()
        book_list = self.app.get(
            reverse('book-list')
        )
        assert str(book.artist) in book_list


class BookDetailTest(WebTest):

    def setUp(self):
        self.book = BookFactory.create()

    @property
    def book_detail(self):
        return self.app.get(self.book.get_absolute_url())

    def test_title(self):
        assert self.book.title in self.book_detail

    def test_artist(self):
        assert str(self.book.artist) in self.book_detail

    def test_artist_link(self):
        self.book_detail.click(
            str(self.book.artist),
            href=self.book.artist.get_absolute_url(),
        )

    def test_date(self):
        assert str(self.book.date.year) in self.book_detail

    def test_date_text_overrides_date(self):
        year, month, day = (3000, 1, 1)
        date = datetime.datetime(year, month, day)
        self.book = BookFactory(date_text='some text', date=date)
        assert str(year) not in self.book_detail

    def test_buy_link(self):
        self.book.price = 10
        self.book.save()
        assert 'Buy for $10' in self.book_detail

    def test_description(self):
        assert self.book.description in self.book_detail
