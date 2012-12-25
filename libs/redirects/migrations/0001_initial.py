# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    needed_by = (
        ('artists', '0001_initial'),
        ('exhibitions', '0001_initial'),
        ('press', '0001_initial'),
        ('updates', '0001_initial'),
    )


    def forwards(self, orm):
        # Adding model 'Redirect'
        db.create_table('django_redirect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sites.Site'])),
            ('old_path', self.gf('django.db.models.fields.CharField')(max_length=2000, db_index=True)),
            ('new_path', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
        ))
        db.send_create_signal('redirects', ['Redirect'])

        # Adding unique constraint on 'Redirect', fields ['site', 'old_path']
        db.create_unique('django_redirect', ['site_id', 'old_path'])


    def backwards(self, orm):
        # Removing unique constraint on 'Redirect', fields ['site', 'old_path']
        db.delete_unique('django_redirect', ['site_id', 'old_path'])

        # Deleting model 'Redirect'
        db.delete_table('django_redirect')


    models = {
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
        }
    }

    complete_apps = ['redirects']
