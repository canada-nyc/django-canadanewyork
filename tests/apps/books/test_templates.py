import re
import datetime

from django_webtest import WebTest
from django.core.urlresolvers import reverse
from webtest.app import AppError

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
            href=reverse('book-list')
        )

    def test_link(self):
        Book = BookFactory.create()
        book_list = self.app.get(
            reverse('book-list')
        )

        # will raise AppError when hits 404, because index link is not a real
        # page, but a mailto link
        with self.assertRaises(AppError):
            book_list.click(
                unicode(Book),
                href=re.escape(Book.get_purchase_url()),
            )

    def test_artist_name_in(self):
        Book = BookFactory.create()
        book_list = self.app.get(
            reverse('book-list')
        )

        self.assertIn(unicode(Book.artist), book_list)


    def test_date_text(self):
        Book = BookFactory(date_text='some text')
        book_list = self.app.get(
            reverse('book-list')
        )
        self.assertIn(Book.date_text, book_list)

    def test_date_text_overrides_date(self):
        year, month, day = (3000, 1, 1)
        date = datetime.datetime(year, month, day)
        Book = BookFactory(date_text='some text', date=date)
        book_list = self.app.get(
            reverse('book-list')
        )
        self.assertNotIn(str(year), book_list)

