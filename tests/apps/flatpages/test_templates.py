from django.core.urlresolvers import reverse
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site

from django_webtest import WebTest


class ContactTest(WebTest):
    def setUp(self):
        self.FlatPage = FlatPage.objects.create(
            url=reverse('contact'),
            title='_',
            content='some content',
        )
        self.FlatPage.sites.add(Site.objects.get_current())

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

    def test_flatpage_content(self):
        exhibition_current = self.app.get(
            reverse('contact')
        )

        self.assertIn(self.FlatPage.content, exhibition_current)

    url = reverse('contact')
