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
            ('redirect', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['redirects.Redirect'], unique=True, null=True, blank=True)),
            ('old_path', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('post_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('slug', self.gf('apps.slugify.fields.SlugifyField')(max_length=50, populate_from=None)),
        ))
        db.send_create_signal('updates', ['Update'])

        # Adding model 'UpdatePhoto'
        db.create_table('updates_updatephoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('update', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['updates.Update'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('updates', ['UpdatePhoto'])


    def backwards(self, orm):
        # Deleting model 'Update'
        db.delete_table('updates_update')

        # Deleting model 'UpdatePhoto'
        db.delete_table('updates_updatephoto')


    models = {
        'redirects.redirect': {
            'Meta': {'ordering': "('old_path',)", 'unique_together': "(('site', 'old_path'),)", 'object_name': 'Redirect', 'db_table': "'django_redirect'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'old_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'old_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'redirect': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['redirects.Redirect']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
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