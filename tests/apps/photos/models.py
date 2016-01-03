from django.db import models

from django_fake_model import models as f
import simpleimages.trackers

from apps.photos.models import ArtworkPhoto


class MockRelated(f.FakeModel):
    pass


class MockPhoto(f.FakeModel, ArtworkPhoto):
    content_object = models.ForeignKey(MockRelated)


simpleimages.trackers.track_model(MockPhoto)
