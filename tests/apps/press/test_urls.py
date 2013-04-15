from django.test import TestCase
from django.core.urlresolvers import reverse

from .factories import PressFactory


class PressUrlTest(TestCase):
    def test_detail(self):
        Press = PressFactory.create()
        self.assertEqual(
            Press.get_absolute_url(),
            reverse('press-detail', kwargs={'slug': Press.slug})
        )
