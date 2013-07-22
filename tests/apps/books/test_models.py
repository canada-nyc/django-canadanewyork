from django.test import TestCase

from .factories import BookFactory


class BookGetPurchaseUrl(TestCase):
    def test_full_content(self):
        book = BookFactory.create()
        url = (
            'mailto:gallery%40canadanewyork.com'
            '?subject=Purchase%20Book'
            '&body=Hello%0AI%20am%20interested%20in%20buying%20{}%20{}%3A{}.'
        )
        url_with_data = url.format(
            book.artist.first_name,
            book.artist.last_name,
            book.title
        )
        self.assertEqual(book.get_purchase_url(), url_with_data)
