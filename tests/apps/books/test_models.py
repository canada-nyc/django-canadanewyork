import urllib.parse

from django.test import TestCase

from .factories import BookFactory


class BookGetPurchaseUrl(TestCase):
    def test_full_content(self):
        book = BookFactory.create(title="hey")
        url = (
            'mailto:gallery%40canadanewyork.com'
            '?subject=Purchase%20Book'
            '&body=Hello%0AI%20am%20interested%20in%20buying%20{}%20{}%3A%20{}.'
            '%20Can%20you%20please%20contact%20me%20for%20pricing%20and%20availability%3F'
        ).format(
            *map(
                urllib.parse.quote,
                [
                    book.artist.first_name,
                    book.artist.last_name,
                    book.title
                ]
            )
        )
        assert book.get_purchase_url() == url
