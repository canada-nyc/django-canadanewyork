# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Photo.year'
        db.add_column(u'photos_photo', 'year',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=400, blank=True),
                      keep_default=False)

        # Adding field 'Photo.medium'
        db.add_column(u'photos_photo', 'medium',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=400, blank=True),
                      keep_default=False)

        # Adding field 'Photo.height'
        db.add_column(u'photos_photo', 'height',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'Photo.width'
        db.add_column(u'photos_photo', 'width',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True),
                      keep_default=False)

        # Adding field 'Photo.depth'
        db.add_column(u'photos_photo', 'depth',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Photo.year'
        db.delete_column(u'photos_photo', 'year')

        # Deleting field 'Photo.medium'
        db.delete_column(u'photos_photo', 'medium')

        # Deleting field 'Photo.height'
        db.delete_column(u'photos_photo', 'height')

        # Deleting field 'Photo.width'
        db.delete_column(u'photos_photo', 'width')

        # Deleting field 'Photo.depth'
        db.delete_column(u'photos_photo', 'depth')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'photos.photo': {
            'Meta': {'ordering': "['position']", 'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'depth': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'height': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1000'}),
            'large_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'large_image_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'large_image_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'thumbnail_image_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail_image_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'width': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'})
        }
    }

    complete_apps = ['photos']