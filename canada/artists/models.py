import os

from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify

from canada.functions import cap


class Artist( models.Model ):
    first_name = models.CharField( max_length = 30 )
    last_name = models.CharField( max_length = 30 )
    slug = models.SlugField(blank=True, editable=False)
    visible = models.BooleanField(default=False, help_text="Whether it appears in the Artists list")

    class Meta:
        ordering = ['last_name', 'first_name']
        unique_together = ( "first_name", "last_name" )

    def __unicode__( self ):
        return u'%s %s' % ( self.first_name, self.last_name )

    def save(self):
        cap(self,'first_name', 'last_name')
        self.slug = slugify('-'.join([self.first_name, self.last_name]))
        super(Artist,self).save()


    @permalink
    def get_absolute_url( self ):
        return ( 'artist-single', (), {
            'slug': self.slug,
            })


class ArtistPhoto( models.Model ):
    def image_path(instance, filename):
        return os.path.join('artists', instance.artist.slug, filename)

    artist = models.ForeignKey( Artist )
    image = models.ImageField( upload_to = image_path )
    title = models.CharField( max_length = 50 )
    medium = models.CharField( blank = True, max_length = 50 )
    year = models.PositiveIntegerField( null = True, blank = True )
    length = models.PositiveIntegerField( null = True, blank = True, help_text = '(in inches)' )
    width = models.PositiveIntegerField( null = True, blank = True, help_text = '(in inches)' )
    position = models.PositiveSmallIntegerField( "Position" )

    class Meta:
        ordering = ['position']

    def __unicode__( self ):
            return u'%s by %s' % ( self.title, self.artist )

    def save(self):
        cap(self,'title')
        super(Artist,self).save()
