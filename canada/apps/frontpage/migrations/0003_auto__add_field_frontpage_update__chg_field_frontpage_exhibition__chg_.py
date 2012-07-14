# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Frontpage.update'
        db.add_column('frontpage_frontpage', 'update',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['updates.Update'], null=True, blank=True),
                      keep_default=False)


        # Changing field 'Frontpage.exhibition'
        db.alter_column('frontpage_frontpage', 'exhibition_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exhibitions.Exhibition'], null=True))

        # Changing field 'Frontpage.exhibition_image'
        db.alter_column('frontpage_frontpage', 'exhibition_image_id', self.gf('smart_selects.db_fields.ChainedForeignKey')(to=orm['updates.UpdatePhoto'], null=True))

        # Changing field 'Frontpage.date_added'
        db.alter_column('frontpage_frontpage', 'date_added', self.gf('django.db.models.fields.DateField')(auto_now_add=True))

    def backwards(self, orm):
        # Deleting field 'Frontpage.update'
        db.delete_column('frontpage_frontpage', 'update_id')


        # User chose to not deal with backwards NULL issues for 'Frontpage.exhibition'
        raise RuntimeError("Cannot reverse this migration. 'Frontpage.exhibition' and its values cannot be restored.")

        # Changing field 'Frontpage.exhibition_image'
        db.alter_column('frontpage_frontpage', 'exhibition_image_id', self.gf('smart_selects.db_fields.ChainedForeignKey')(to=orm['exhibitions.ExhibitionPhoto'], null=True))

        # Changing field 'Frontpage.date_added'
        db.alter_column('frontpage_frontpage', 'date_added', self.gf('django.db.models.fields.DateField')())

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
        'frontpage.frontpage': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Frontpage'},
            'activated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exhibition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exhibitions.Exhibition']", 'null': 'True', 'blank': 'True'}),
            'exhibition_image': ('smart_selects.db_fields.ChainedForeignKey', [], {'to': "orm['updates.UpdatePhoto']", 'null': 'True', 'blank': 'True'}),
            'extra_text': ('django.db.models.fields.TextField', [], {'max_length': '800', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'update': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['updates.Update']", 'null': 'True', 'blank': 'True'}),
            'uploaded_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
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

    complete_apps = ['frontpage']