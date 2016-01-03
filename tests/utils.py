from datetime import date
import random
from django.core.files.base import ContentFile

from factory.fuzzy import BaseFuzzyAttribute
import factory


def random_date(start_date=date(2005, 1, 1), end_date=date.today()):
    return date.fromordinal(random.randint(start_date.toordinal(), end_date.toordinal()))


class FuzzyDate(BaseFuzzyAttribute):
    def __init__(self, start_date=date(2005, 1, 1), end_date=date.today(), **kwargs):
        super(FuzzyDate, self).__init__(**kwargs)
        self.start_date = start_date.toordinal()
        self.end_date = end_date.toordinal()

    def fuzz(self):
        return date.fromordinal(random.randint(self.start_date, self.end_date))


def django_image(**params):
    return ContentFile(factory.django.ImageField()._make_data(params))
