# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Artist'
        db.create_table('artists_artist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('resume', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('slug', self.gf('apps.slugify.fields.SlugifyField')(max_length=50, populate_from=('first_name', 'last_name'))),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('artists', ['Artist'])

        # Adding unique constraint on 'Artist', fields ['first_name', 'last_name']
        db.create_unique('artists_artist', ['first_name', 'last_name'])

        # Adding model 'ArtistPhoto'
        db.create_table('artists_artistphoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['artists.Artist'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('artists', ['ArtistPhoto'])


    def backwards(self, orm):
        # Removing unique constraint on 'Artist', fields ['first_name', 'last_name']
        db.delete_unique('artists_artist', ['first_name', 'last_name'])

        # Deleting model 'Artist'
        db.delete_table('artists_artist')

        # Deleting model 'ArtistPhoto'
        db.delete_table('artists_artistphoto')


    models = {
        'artists.artist': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Artist'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'resume': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('apps.slugify.fields.SlugifyField', [], {'max_length': '50', 'populate_from': "('first_name', 'last_name')"}),
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