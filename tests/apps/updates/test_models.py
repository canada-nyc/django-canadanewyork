from django.test import TestCase

from .factories import UpdateFactory


class UpdateTest(TestCase):
    def test_create_update(self):
        UpdateFactory()
