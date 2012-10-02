from django.test import TestCase

from .factories import PressFactory


class PressTest(TestCase):
    def test_create_press(self):
        PressFactory()
