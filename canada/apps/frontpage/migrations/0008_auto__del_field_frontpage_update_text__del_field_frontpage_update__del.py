# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Frontpage.update_text'
        db.delete_column('frontpage_frontpage', 'update_text')

        # Deleting field 'Frontpage.update'
        db.delete_column('frontpage_frontpage', 'update_id')

        # Deleting field 'Frontpage.custom_title'
        db.delete_column('frontpage_frontpage', 'custom_title')

        # Deleting field 'Frontpage.exhibition_text'
        db.delete_column('frontpage_frontpage', 'exhibition_text')

        # Deleting field 'Frontpage.update_image'
        db.delete_column('frontpage_frontpage', 'update_image_id')


        # Changing field 'Frontpage.exhibition'
        db.alter_column('frontpage_frontpage', 'exhibition_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['exhibitions.Exhibition']))

    def backwards(self, orm):
        # Adding field 'Frontpage.update_text'
        db.add_column('frontpage_frontpage', 'update_text',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Frontpage.update'
        db.add_column('frontpage_frontpage', 'update',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['updates.Update'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Frontpage.custom_title'
        db.add_column('frontpage_frontpage', 'custom_title',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Frontpage.exhibition_text'
        db.add_column('frontpage_frontpage', 'exhibition_text',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Frontpage.update_image'
        db.add_column('frontpage_frontpage', 'update_image',
                      self.gf('smart_selects.db_fields.ChainedForeignKey')(to=orm['updates.UpdatePhoto'], null=True, blank=True),
                      keep_default=False)


        # Changing field 'Frontpage.exhibition'
        db.alter_column('frontpage_frontpage', 'exhibition_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exhibitions.Exhibition'], null=True))

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
            'dimensions': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'exhibition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['exhibitions.Exhibition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'frontpage.frontpage': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Frontpage'},
            'UniqueBooleanField': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exhibition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exhibitions.Exhibition']"}),
            'exhibition_image': ('smart_selects.db_fields.ChainedForeignKey', [], {'to': "orm['exhibitions.ExhibitionPhoto']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '800', 'null': 'True', 'blank': 'True'}),
            'uploaded_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['frontpage']