from django_webtest import WebTest
from django.core.urlresolvers import reverse

from .factories import UpdateFactory


class UpdateListTest(WebTest):
    def test_reverse(self):
        self.app.get(
            reverse('update-list')
        )

    def test_nav_click(self):
        press_list = self.app.get(
            reverse('update-list')
        )
        press_list.click(
            'Updates',
            href=reverse('update-list')
        )

    def test_click_indivual(self):
        Update = UpdateFactory()
        update_list = self.app.get(
            reverse('update-list')
        )
        update_list.click(
            href=reverse('update-detail', kwargs={'pk': Update.pk})
        )


class UpdateDetailTest(WebTest):
    def test_description(self):
        Update = UpdateFactory(description='description')
        update_detail = self.app.get(Update.get_absolute_url())
        assert Update.description in update_detail
