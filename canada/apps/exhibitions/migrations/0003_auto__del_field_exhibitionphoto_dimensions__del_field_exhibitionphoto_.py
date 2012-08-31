# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ExhibitionPhoto.dimensions'
        db.delete_column('exhibitions_exhibitionphoto', 'dimensions')

        # Deleting field 'ExhibitionPhoto.year'
        db.delete_column('exhibitions_exhibitionphoto', 'year')

        # Deleting field 'ExhibitionPhoto.medium'
        db.delete_column('exhibitions_exhibitionphoto', 'medium')

        # Adding field 'ExhibitionPhoto.caption'
        db.add_column('exhibitions_exhibitionphoto', 'caption',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)


        # Changing field 'ExhibitionPhoto.title'
        db.alter_column('exhibitions_exhibitionphoto', 'title', self.gf('django.db.models.fields.CharField')(max_length=20))

    def backwards(self, orm):
        # Adding field 'ExhibitionPhoto.dimensions'
        db.add_column('exhibitions_exhibitionphoto', 'dimensions',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True),
                      keep_default=False)

        # Adding field 'ExhibitionPhoto.year'
        db.add_column('exhibitions_exhibitionphoto', 'year',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'ExhibitionPhoto.medium'
        db.add_column('exhibitions_exhibitionphoto', 'medium',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Deleting field 'ExhibitionPhoto.caption'
        db.delete_column('exhibitions_exhibitionphoto', 'caption')


        # Changing field 'ExhibitionPhoto.title'
        db.alter_column('exhibitions_exhibitionphoto', 'title', self.gf('django.db.models.fields.CharField')(max_length=50))

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
        'exhibitions.exhibition': {
            'Meta': {'ordering': "['-start_date']", 'object_name': 'Exhibition'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'exhibitions'", 'symmetrical': 'False', 'to': "orm['artists.Artist']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'exhibitions.exhibitionphoto': {
            'Meta': {'ordering': "['position']", 'object_name': 'ExhibitionPhoto'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'exhibition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['exhibitions.Exhibition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        }
    }

    complete_apps = ['exhibitions']