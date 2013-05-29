from django.db import models
from django.contrib.contenttypes import generic

from apps.photos.models import Photo


class RelatedPhotoModel(models.Model):

    photos = generic.GenericRelation(Photo)
