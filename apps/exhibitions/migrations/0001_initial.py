# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Exhibition'
        db.create_table(u'exhibitions_exhibition', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('slug', self.gf('libs.slugify.fields.SlugifyField')(unique=True, max_length=251, populate_from=('get_year', 'name'))),
            ('current', self.gf('libs.unique_boolean.fields.UniqueBooleanField')(default=True)),
            ('press_release_photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'exhibitions', ['Exhibition'])

        # Adding M2M table for field artists on 'Exhibition'
        db.create_table(u'exhibitions_exhibition_artists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('exhibition', models.ForeignKey(orm[u'exhibitions.exhibition'], null=False)),
            ('artist', models.ForeignKey(orm[u'artists.artist'], null=False))
        ))
        db.create_unique(u'exhibitions_exhibition_artists', ['exhibition_id', 'artist_id'])


    def backwards(self, orm):
        # Deleting model 'Exhibition'
        db.delete_table(u'exhibitions_exhibition')

        # Removing M2M table for field artists on 'Exhibition'
        db.delete_table('exhibitions_exhibition_artists')


    models = {
        u'artists.artist': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Artist'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'resume': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('libs.slugify.fields.SlugifyField', [], {'max_length': '251', 'populate_from': "('first_name', 'last_name')"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'exhibitions.exhibition': {
            'Meta': {'ordering': "['-start_date']", 'object_name': 'Exhibition'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'exhibitions'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['artists.Artist']"}),
            'current': ('libs.unique_boolean.fields.UniqueBooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'press_release_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('libs.slugify.fields.SlugifyField', [], {'unique': 'True', 'max_length': '251', 'populate_from': "('get_year', 'name')"}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'photos.photo': {
            'Meta': {'ordering': "['position']", 'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1000'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'})
        }
    }

    complete_apps = ['exhibitions']