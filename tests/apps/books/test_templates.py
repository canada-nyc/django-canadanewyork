import re
import datetime

import pytest
from webtest.app import AppError

from django.core.urlresolvers import reverse

from django_webtest import WebTest

from .factories import BookFactory


class BookListTest(WebTest):

    def test_reverse(self):
        self.app.get(
            reverse('book-list')
        )

    def test_nav_click(self):
        book_list = self.app.get(
            reverse('book-list')
        )
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
        # will raise AppError when hits 404, because index link is not a real
        # page, but a mailto link
        with pytest.raises(AppError):
            self.book_detail.click(
                'Buy',
                href=re.escape(self.book.get_purchase_url())
            )

    def test_description(self):
        assert self.book.description in self.book_detail
