# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ArtistPhoto.dimensions'
        db.delete_column('artists_artistphoto', 'dimensions')

        # Deleting field 'ArtistPhoto.year'
        db.delete_column('artists_artistphoto', 'year')

        # Deleting field 'ArtistPhoto.medium'
        db.delete_column('artists_artistphoto', 'medium')

        # Adding field 'ArtistPhoto.caption'
        db.add_column('artists_artistphoto', 'caption',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)


        # Changing field 'ArtistPhoto.title'
        db.alter_column('artists_artistphoto', 'title', self.gf('django.db.models.fields.CharField')(max_length=20))

    def backwards(self, orm):
        # Adding field 'ArtistPhoto.dimensions'
        db.add_column('artists_artistphoto', 'dimensions',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True),
                      keep_default=False)

        # Adding field 'ArtistPhoto.year'
        db.add_column('artists_artistphoto', 'year',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'ArtistPhoto.medium'
        db.add_column('artists_artistphoto', 'medium',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Deleting field 'ArtistPhoto.caption'
        db.delete_column('artists_artistphoto', 'caption')


        # Changing field 'ArtistPhoto.title'
        db.alter_column('artists_artistphoto', 'title', self.gf('django.db.models.fields.CharField')(max_length=50))

    models = {
        'artists.artist': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Artist'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'resume': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'artists.artistphoto': {
            'Meta': {'ordering': "['position']", 'object_name': 'ArtistPhoto'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['artists.Artist']"}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        }
    }

    complete_apps = ['artists']