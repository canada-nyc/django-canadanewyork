from django.test import TestCase

from .models import UniqueBooleanModel


@UniqueBooleanModel.fake_me
class UniqueBooleanTest(TestCase):

    def test_wont_change_to_true(self):
        UniqueBooleanModel.objects.create(unique_boolean=False)
        model = UniqueBooleanModel.objects.all()[0]
        assert not model.unique_boolean

    def test_adding_another_will_change(self):
        UniqueBooleanModel.objects.create(unique_boolean=True)
        # When saving the second model, it should turn the first ones boolean to false
        UniqueBooleanModel.objects.create(unique_boolean=True)

        # Should be the only model with True now
        UniqueBooleanModel.objects.get(unique_boolean=True)
