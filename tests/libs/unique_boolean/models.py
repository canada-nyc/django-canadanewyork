from django_fake_model import models as f

from libs.unique_boolean.fields import UniqueBooleanField


class UniqueBooleanModel(f.FakeModel):
    unique_boolean = UniqueBooleanField()

    def __str__(self):
        return str(self.unique_boolean)
