# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Contact.list'
        db.delete_column('bulkmail_contact', 'list_id')

        # Adding field 'Contact.contact_list'
        db.add_column('bulkmail_contact', 'contact_list',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='contacts', to=orm['bulkmail.ContactList']),
                      keep_default=False)

        # Deleting field 'Message.list'
        db.delete_column('bulkmail_message', 'list_id')

        # Adding field 'Message.contact_list'
        db.add_column('bulkmail_message', 'contact_list',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['bulkmail.ContactList']),
                      keep_default=False)

        # Adding unique constraint on 'ContactList', fields ['name']
        db.create_unique('bulkmail_contactlist', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'ContactList', fields ['name']
        db.delete_unique('bulkmail_contactlist', ['name'])


        # User chose to not deal with backwards NULL issues for 'Contact.list'
        raise RuntimeError("Cannot reverse this migration. 'Contact.list' and its values cannot be restored.")
        # Deleting field 'Contact.contact_list'
        db.delete_column('bulkmail_contact', 'contact_list_id')


        # User chose to not deal with backwards NULL issues for 'Message.list'
        raise RuntimeError("Cannot reverse this migration. 'Message.list' and its values cannot be restored.")
        # Deleting field 'Message.contact_list'
        db.delete_column('bulkmail_message', 'contact_list_id')


    models = {
        'bulkmail.contact': {
            'Meta': {'ordering': "['contact_list', 'email']", 'object_name': 'Contact'},
            'contact_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contacts'", 'to': "orm['bulkmail.ContactList']"}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'bulkmail.contactlist': {
            'Meta': {'ordering': "['name']", 'object_name': 'ContactList'},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
