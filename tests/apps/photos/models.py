
from django.db import models

import simpleimages.trackers

from apps.photos.models import ArtworkPhoto


class MockRelated(models.Model):
    pass


class MockPhoto(ArtworkPhoto):
    content_object = models.ForeignKey(MockRelated)


simpleimages.trackers.track_model(MockPhoto)
