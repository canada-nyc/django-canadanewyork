import datetime
import re

from django_webtest import WebTest
from django.core.files.base import ContentFile

from .factories import PressFactory


class PressDetailTest(WebTest):
    def test_unicode(self):
        Press = PressFactory(content='content stuff')
        press_detail = self.app.get(Press.get_absolute_url())
        assert str(Press) in press_detail

    def test_content(self):
        Press = PressFactory(content='content stuff')
        press_detail = self.app.get(Press.get_absolute_url())
        assert Press.content in press_detail

    def test_content_file_path(self):
        Press = PressFactory()
        Press.content_file.save('file.txt', ContentFile("my string content"))
        press_detail = self.app.get(Press.get_absolute_url())
        press_detail.click(
            href=re.escape(Press.content_file.url),
        )

    def test_content_link_path(self):
        Press = PressFactory(content_link='http://domain.com')
        press_detail = self.app.get(Press.get_absolute_url())
        press_detail.click(
            href=re.escape(Press.content_link),
        )

    def test_date_text(self):
        Press = PressFactory(content='_', date_text='some text')
        press_detail = self.app.get(Press.get_absolute_url())
        assert Press.date_text in press_detail

    def test_date_text_overrides_date(self):
        year, month, day = (3000, 1, 1)
        date = datetime.datetime(year, month, day)
        date_text = 'Something or other'
        Press = PressFactory(content='_', date_text=date_text, date=date)
        press_detail = self.app.get(Press.get_absolute_url())
        assert date_text in press_detail

    def test_pages_range_displayed(self):
        Press = PressFactory(content='_', pages_range='some text')
        press_detail = self.app.get(Press.get_absolute_url())
        assert Press.pages_range in press_detail
