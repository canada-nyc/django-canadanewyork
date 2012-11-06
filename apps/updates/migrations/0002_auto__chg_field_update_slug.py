# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Update.slug'
        db.alter_column('updates_update', 'slug', self.gf('apps.slugify.fields.SlugifyField')(max_length=50, populate_from=None))

    def backwards(self, orm):

        # Changing field 'Update.slug'
        db.alter_column('updates_update', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50))

    models = {
        'updates.update': {
            'Meta': {'ordering': "['-post_date']", 'object_name': 'Update'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'slug': ('apps.slugify.fields.SlugifyField', [], {'max_length': '50', 'populate_from': 'None'})
        },
        'updates.updatephoto': {
            'Meta': {'ordering': "['position']", 'object_name': 'UpdatePhoto'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'update': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['updates.Update']"})
        }
    }

    complete_apps = ['updates']