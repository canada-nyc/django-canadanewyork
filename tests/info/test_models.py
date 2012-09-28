from django.test import TestCase

from .factories import InfoFactory


class InfoTest(TestCase):
    def test_create_info(self):
        InfoFactory()
