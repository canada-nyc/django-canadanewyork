from django.test import TestCase
from django.test.utils import override_settings
from django.conf import settings
from django.core.management import call_command
from django.db.models import loading


from .models import UniqueBooleanModel


@override_settings(SOUTH_TESTS_MIGRATE=False)
@override_settings(INSTALLED_APPS=settings.INSTALLED_APPS + ('tests.fields',))
class UniqueBooleanTest(TestCase):
    def setUp(self):
        loading.cache.loaded = False
        call_command('syncdb', verbosity=0)

    def test_field(self):
        # Create one model
        UniqueBooleanModel(unique_boolean=False).save()
        # Assert that it is True
        UniqueBooleanModel.objects.get(unique_boolean=True)

        # Create another UniqueBooleanModel with True
        self.m1 = UniqueBooleanModel(unique_boolean=True)
        self.m1.save()
        # Should be the only model with True
        self.assertEqual(UniqueBooleanModel.objects.get(unique_boolean=True), self.m1)

        # Disable True on model1, shouldnt actually disable
        self.m1.unique_boolean = False
        self.m1.save()
        # Still should be only model with True
        self.assertEqual(UniqueBooleanModel.objects.get(unique_boolean=True), self.m1)
