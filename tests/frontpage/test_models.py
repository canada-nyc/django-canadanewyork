from django.test import TestCase

from .factories import FrontpageFactory


class FrontpageTest(TestCase):
    def test_create_Frontpage(self):
        FrontpageFactory()
        FrontpageFactory()
