# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Info'
        db.create_table('info_info', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('activated', self.gf('apps.unique_boolean.fields.UniqueBooleanField')(default=False)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=800, null=True, blank=True)),
        ))
        db.send_create_signal('info', ['Info'])


    def backwards(self, orm):
        # Deleting model 'Info'
        db.delete_table('info_info')


    models = {
        'info.info': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'Info'},
            'activated': ('apps.unique_boolean.fields.UniqueBooleanField', [], {'default': 'False'}),
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '800', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['info']