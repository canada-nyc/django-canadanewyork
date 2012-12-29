from django_webtest import WebTest

from .factories import FrontpageFactory


class FrontpageTest(WebTest):

    def test_display(self):
        Frontpage = FrontpageFactory()
        frontpage_detail = self.app.get('/')
        exhibition_detail = frontpage_detail.click(href=Frontpage.exhibition.get_absolute_url())
        assert Frontpage.exhibition.name in exhibition_detail
