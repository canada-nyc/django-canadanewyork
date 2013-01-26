from django.test import TestCase

from .models import UniqueBooleanModel
from ...common.base_test import AddAppMixin


class UniqueBooleanTest(AddAppMixin, TestCase):
    custom_apps = ('tests.libs.unique_boolean',)

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

    def test_model_method(self):
        UniqueBooleanModel(unique_boolean=False).save()
        model = UniqueBooleanModel.objects.get(unique_boolean=True)

        self.assertEqual(
            model._get_unique_boolean_value(),
            True
        )
