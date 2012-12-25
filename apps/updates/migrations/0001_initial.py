# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Update'
        db.create_table('updates_update', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=800)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('post_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('slug', self.gf('libs.slugify.fields.SlugifyField')(max_length=1000, populate_from=None)),
            ('old_path', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('redirect', self.gf('libs.content_redirects.fields.RedirectField')(unique=True, null=True, on_delete=models.SET_NULL, blank=True)),
        ))
        db.send_create_signal('updates', ['Update'])


    def backwards(self, orm):
        # Deleting model 'Update'
        db.delete_table('updates_update')


    models = {
        'common.photo': {
            'Meta': {'ordering': "['position']", 'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1000'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'redirects.redirect': {
            'Meta': {'ordering': "('old_path',)", 'unique_together': "(('site', 'old_path'),)", 'object_name': 'Redirect', 'db_table': "'django_redirect'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_path': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'old_path': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sites.Site']"})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'updates.update': {
            'Meta': {'ordering': "['-post_date']", 'object_name': 'Update'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '800'}),
            'old_path': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'redirect': ('libs.content_redirects.fields.RedirectField', [], {'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'slug': ('libs.slugify.fields.SlugifyField', [], {'max_length': '1000', 'populate_from': 'None'})
        }
    }

    complete_apps = ['updates']