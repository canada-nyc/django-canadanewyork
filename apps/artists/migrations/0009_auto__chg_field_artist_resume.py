# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Artist.resume'
        db.alter_column(u'artists_artist', 'resume', self.gf('libs.ckeditor.fields.CKEditorField')())

    def backwards(self, orm):

        # Changing field 'Artist.resume'
        db.alter_column(u'artists_artist', 'resume', self.gf('django.db.models.fields.TextField')())

    models = {
        u'artists.artist': {
            'Meta': {'ordering': "['-visible', 'last_name', 'first_name']", 'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Artist'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'resume': ('libs.ckeditor.fields.CKEditorField', [], {'blank': 'True'}),
            'resume_file': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'slug': ('libs.slugify.fields.SlugifyField', [], {'max_length': '251', 'populate_from': "('first_name', 'last_name')"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'artists.artistphoto': {
            'Meta': {'ordering': "['position']", 'object_name': 'ArtistPhoto'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'photos'", 'to': u"orm['artists.Artist']"}),
            'date': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'depth': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
            'dimensions_text': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'}),
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
            'width': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4', 'blank': 'True'})
        }
    }

    complete_apps = ['artists']