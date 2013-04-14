from django.test import TestCase
from django.core.urlresolvers import reverse

from .factories import ExhibitionFactory


class ExhibitionUrlTest(TestCase):
    def test_detail(self):
        Exhibition = ExhibitionFactory.create()
        self.assertEqual(
            Exhibition.get_absolute_url(),
            reverse('exhibition-detail', kwargs={'slug': Exhibition.slug})
        )
