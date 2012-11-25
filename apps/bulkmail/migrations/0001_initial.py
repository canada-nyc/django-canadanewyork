# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ContactList'
        db.create_table('bulkmail_contactlist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('default', self.gf('libs.unique_boolean.fields.UniqueBooleanField')(default=False)),
        ))
        db.send_create_signal('bulkmail', ['ContactList'])

        # Adding model 'Message'
        db.create_table('bulkmail_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('contact_list', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bulkmail.ContactList'])),
        ))
        db.send_create_signal('bulkmail', ['Message'])

        # Adding model 'Contact'
        db.create_table('bulkmail_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('contact_list', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contacts', to=orm['bulkmail.ContactList'])),
        ))
        db.send_create_signal('bulkmail', ['Contact'])


    def backwards(self, orm):
        # Deleting model 'ContactList'
        db.delete_table('bulkmail_contactlist')

        # Deleting model 'Message'
        db.delete_table('bulkmail_message')

        # Deleting model 'Contact'
        db.delete_table('bulkmail_contact')


    models = {
        'bulkmail.contact': {
            'Meta': {'ordering': "['contact_list', 'email']", 'object_name': 'Contact'},
            'contact_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contacts'", 'to': "orm['bulkmail.ContactList']"}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'bulkmail.contactlist': {
            'Meta': {'ordering': "['name']", 'object_name': 'ContactList'},
            'default': ('libs.unique_boolean.fields.UniqueBooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'bulkmail.message': {
            'Meta': {'ordering': "['-date_time']", 'object_name': 'Message'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'contact_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bulkmail.ContactList']"}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['bulkmail']