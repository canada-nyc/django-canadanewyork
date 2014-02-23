from django.core.urlresolvers import reverse

from django_webtest import WebTest

from apps.custompages.models import CustomPage


class ContactTest(WebTest):

    def setUp(self):
        self.CustomPage = CustomPage.objects.create(
            path=reverse('contact'),
            content='some content',
        )

    def test_reverse(self):
        self.app.get(
            reverse('contact')
        )

    def test_nav_click(self):
        contact = self.app.get(
            reverse('contact')
        )
        contact.click(
            'Contact',
            href=reverse('contact')
        )

    def test_content(self):
        exhibition_current = self.app.get(
            reverse('contact')
        )

        self.assertIn(self.CustomPage.content, exhibition_current)

    def test_no_content(self):
        self.CustomPage.delete()

        self.app.get(
            reverse('contact')
        )
