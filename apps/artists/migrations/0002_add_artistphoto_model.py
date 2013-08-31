# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ArtistPhoto'
        db.create_table(u'artists_artistphoto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=400, blank=True)),
            ('caption', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=1000)),
            ('thumbnail_image', self.gf('django.db.models.fields.files.ImageField')(max_length=1000, null=True, blank=True)),
            ('large_image', self.gf('django.db.models.fields.files.ImageField')(max_length=1000, null=True, blank=True)),
            ('thumbnail_image_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('thumbnail_image_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('large_image_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('large_image_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('medium', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('height', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('depth', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('content_object', self.gf('django.db.models.fields.related.ForeignKey')(related_name='new_photos', to=orm['artists.Artist'])),
        ))
        db.send_create_signal(u'artists', ['ArtistPhoto'])


    def backwards(self, orm):
        # Deleting model 'ArtistPhoto'
        db.delete_table(u'artists_artistphoto')


    models = {
        u'artists.artist': {
            'Meta': {'ordering': "['-visible', 'last_name', 'first_name']", 'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Artist'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'resume': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('libs.slugify.fields.SlugifyField', [], {'max_length': '251', 'populate_from': "('first_name', 'last_name')"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'artists.artistphoto': {
            'Meta': {'object_name': 'ArtistPhoto'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'new_photos'", 'to': u"orm['artists.Artist']"}),
            'depth': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1000'}),
            'large_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'large_image_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'large_image_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'thumbnail_image_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail_image_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'width': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'photos.photo': {
            'Meta': {'object_name': 'Photo'},
            'artist_text': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'depth': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1000'}),
            'large_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'large_image_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'large_image_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'thumbnail_image_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail_image_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'width': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['artists']