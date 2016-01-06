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


def FakerTitle(words=3):
    return factory.LazyAttribute(
        lambda _: ' '.join(factory.Faker('words', nb=words).generate({}))
    )


class FakerImageField(factory.django.ImageField):
    def __init__(self, **kwargs):
        random_kwargs = {
            'color': factory.Faker('rgb_color_list').generate({}),
            'height': factory.fuzzy.FuzzyInteger(10, 700).fuzz(),
            'width': factory.fuzzy.FuzzyInteger(10, 700).fuzz(),
        }
        random_kwargs.update(kwargs)
        super().__init__(**random_kwargs)
