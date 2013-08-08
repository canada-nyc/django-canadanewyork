import re

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

