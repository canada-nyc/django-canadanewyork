import os
import datetime

from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify

from canada.artists.models import Artist
from canada.exhibitions.models import Exhibition
from canada.functions import cap


class Update( models.Model ):

    name = models.CharField( max_length = 30, unique_for_year = 'post_date')
    description = models.TextField(blank=True)
    artists = models.ManyToManyField( Artist, blank=True )
    exhibition = models.ForeignKey( Exhibition, blank=True )
    post_date = models.DateTimeField(editable=False)
    slug = models.SlugField(blank=True,editable=False)

    class Meta:
        ordering = ["-post_date"]

    def __unicode__( self ):
        return '%s-%s' % ( self.post_date.strftime( "%Y" ), self.name )

    def save(self, *args, **kwargs):
        cap(self, 'name')
        if not self.id:
            self.post_date = datetime.datetime.today()
        self.slug = slugify(self.name)
        super(Update,self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('press.views.single', (), {
            'slug': self.slug,
            'year': self.post_date.strftime("%Y")
            })

class UpdatePhoto( models.Model ):

    def image_path(instance, filename):
        return os.path.join('updates', str(instance.update.post_date.year), str(instance.update.name), filename)

    update = models.ForeignKey( Update )
    image = models.ImageField( upload_to = image_path )
    caption = models.CharField(max_length=50)
    position = models.PositiveSmallIntegerField( "Position" )

    class Meta:
        ordering = ['position']

    def __unicode__( self ):
        return '%s from %s id: %s' % ( self.caption, self.update, self.id )
