import datetime

import factory

from apps.updates.models import Update
from ...common.factories import DjangoFactory, BasePhotoFactory


class UpdateFactory(DjangoFactory):
    FACTORY_FOR = Update

    name = factory.Sequence(lambda n: 'name{}'.format(n))
    description = '*italics* **bold**'

    post_date = datetime.date.today()

    @factory.post_generation(extract_prefix='photos')
    def create_photos(self, create, extracted, **kwargs):
        if 'n' in kwargs:
            [UpdatePhotoFactory(content_object=self) for _ in range(int(kwargs['n']))]


class UpdatePhotoFactory(BasePhotoFactory):
    content_object = factory.SubFactory(UpdateFactory)
