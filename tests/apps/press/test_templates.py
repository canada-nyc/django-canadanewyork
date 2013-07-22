from django_webtest import WebTest
from django.core.files.base import ContentFile

from .factories import PressFactory


class PressDetailTest(WebTest):
    def test_unicode(self):
        Press = PressFactory(content='content stuff')
        press_detail = self.app.get(Press.get_absolute_url())
        self.assertIn(unicode(Press), press_detail)

    def test_content(self):
        Press = PressFactory(content='content stuff')
        press_detail = self.app.get(Press.get_absolute_url())
        self.assertIn(Press.content, press_detail)

    def test_no_content_cant_get(self):
        Press = PressFactory()
        Press.content_file.save('file.txt', ContentFile("my string content"))
        self.app.get(Press.get_absolute_url(), status=404)
