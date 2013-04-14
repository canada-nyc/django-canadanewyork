from django.test import TestCase
from django.core.urlresolvers import reverse

from .factories import UpdateFactory


class UpdateUrlTest(TestCase):
    def test_detail(self):
        Update = UpdateFactory.create()
        self.assertEqual(
            Update.get_absolute_url(),
            reverse('update-detail', kwargs={'pk': Update.pk})
        )
