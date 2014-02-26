# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'CustomPage.content'
        db.alter_column(u'custompages_custompage', 'content', self.gf('libs.ckeditor.fields.CKEditorField')())

    def backwards(self, orm):

        # Changing field 'CustomPage.content'
        db.alter_column(u'custompages_custompage', 'content', self.gf('django.db.models.fields.TextField')())

    models = {
        u'custompages.custompage': {
            'Meta': {'ordering': "('path',)", 'object_name': 'CustomPage'},
            'content': ('libs.ckeditor.fields.CKEditorField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        }
    }

    complete_apps = ['custompages']