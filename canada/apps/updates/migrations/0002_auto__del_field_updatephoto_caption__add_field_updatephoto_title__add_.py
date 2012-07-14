# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'UpdatePhoto.caption'
        db.delete_column('updates_updatephoto', 'caption')

        # Adding field 'UpdatePhoto.title'
        db.add_column('updates_updatephoto', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'UpdatePhoto.medium'
        db.add_column('updates_updatephoto', 'medium',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'UpdatePhoto.year'
        db.add_column('updates_updatephoto', 'year',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'UpdatePhoto.dimensions'
        db.add_column('updates_updatephoto', 'dimensions',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'UpdatePhoto.caption'
        raise RuntimeError("Cannot reverse this migration. 'UpdatePhoto.caption' and its values cannot be restored.")
        # Deleting field 'UpdatePhoto.title'
        db.delete_column('updates_updatephoto', 'title')

        # Deleting field 'UpdatePhoto.medium'
        db.delete_column('updates_updatephoto', 'medium')

        # Deleting field 'UpdatePhoto.year'
        db.delete_column('updates_updatephoto', 'year')

        # Deleting field 'UpdatePhoto.dimensions'
        db.delete_column('updates_updatephoto', 'dimensions')


    models = {
        'artists.artist': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Artist'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'exhibitions.exhibition': {
            'Meta': {'ordering': "['-start_date']", 'object_name': 'Exhibition'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['artists.Artist']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'updates.update': {
            'Meta': {'ordering': "['-post_date']", 'object_name': 'Update'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['artists.Artist']", 'symmetrical': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'exhibition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exhibitions.Exhibition']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        'updates.updatephoto': {
            'Meta': {'ordering': "['position']", 'object_name': 'UpdatePhoto'},
            'dimensions': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'update': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['updates.Update']"}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['updates']