# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Exhibition.frontpage_text'
        db.delete_column('exhibitions_exhibition', 'frontpage_text')

        # Deleting field 'Exhibition.frontpage_selected_image'
        db.delete_column('exhibitions_exhibition', 'frontpage_selected_image_id')

        # Deleting field 'Exhibition.frontpage_uploaded_image'
        db.delete_column('exhibitions_exhibition', 'frontpage_uploaded_image')

        # Deleting field 'Exhibition.frontpage'
        db.delete_column('exhibitions_exhibition', 'frontpage')

        # Deleting field 'ExhibitionPhoto.caption'
        db.delete_column('exhibitions_exhibitionphoto', 'caption')

        # Adding field 'ExhibitionPhoto.title'
        db.add_column('exhibitions_exhibitionphoto', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'ExhibitionPhoto.medium'
        db.add_column('exhibitions_exhibitionphoto', 'medium',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'ExhibitionPhoto.year'
        db.add_column('exhibitions_exhibitionphoto', 'year',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'ExhibitionPhoto.dimensions'
        db.add_column('exhibitions_exhibitionphoto', 'dimensions',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Exhibition.frontpage_text'
        db.add_column('exhibitions_exhibition', 'frontpage_text',
                      self.gf('django.db.models.fields.TextField')(max_length=800, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Exhibition.frontpage_selected_image'
        db.add_column('exhibitions_exhibition', 'frontpage_selected_image',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='frontpage_selected_image', null=True, to=orm['exhibitions.ExhibitionPhoto'], blank=True),
                      keep_default=False)

        # Adding field 'Exhibition.frontpage_uploaded_image'
        db.add_column('exhibitions_exhibition', 'frontpage_uploaded_image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Exhibition.frontpage'
        db.add_column('exhibitions_exhibition', 'frontpage',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ExhibitionPhoto.caption'
        raise RuntimeError("Cannot reverse this migration. 'ExhibitionPhoto.caption' and its values cannot be restored.")
        # Deleting field 'ExhibitionPhoto.title'
        db.delete_column('exhibitions_exhibitionphoto', 'title')

        # Deleting field 'ExhibitionPhoto.medium'
        db.delete_column('exhibitions_exhibitionphoto', 'medium')

        # Deleting field 'ExhibitionPhoto.year'
        db.delete_column('exhibitions_exhibitionphoto', 'year')

        # Deleting field 'ExhibitionPhoto.dimensions'
        db.delete_column('exhibitions_exhibitionphoto', 'dimensions')


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
        'exhibitions.exhibitionphoto': {
            'Meta': {'ordering': "['position']", 'object_name': 'ExhibitionPhoto'},
            'dimensions': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'exhibition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['exhibitions.Exhibition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['exhibitions']