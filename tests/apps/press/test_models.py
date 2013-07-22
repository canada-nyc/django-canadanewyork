from django.test import TestCase
from django.core.files.base import ContentFile

from .factories import PressFactory


class PressGetContentUrlTest(TestCase):
    def test_blank(self):
        Press = PressFactory.create()
        self.assertFalse(Press.get_content_url())

    def test_content_file(self):
        Press = PressFactory()
        Press.content_file.save('file.txt', ContentFile("my string content"))
        self.assertEqual(Press.get_content_url(), Press.content_file.url)

    def test_content(self):
        Press = PressFactory(content='_')
        self.assertEqual(Press.get_content_url(), Press.get_absolute_url())
