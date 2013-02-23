# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Press'
        db.create_table('press_press', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('content_file', self.gf('django.db.models.fields.files.FileField')(max_length=500, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('exhibition', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='press', null=True, to=orm['exhibitions.Exhibition'])),
            ('slug', self.gf('libs.slugify.fields.SlugifyField')(unique=True, max_length=251, populate_from=('get_year', 'publisher', 'title'))),
        ))
        db.send_create_signal('press', ['Press'])

        # Adding M2M table for field artists on 'Press'
        db.create_table('press_press_artists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('press', models.ForeignKey(orm['press.press'], null=False)),
            ('artist', models.ForeignKey(orm['artists.artist'], null=False))
        ))
        db.create_unique('press_press_artists', ['press_id', 'artist_id'])


    def backwards(self, orm):
        # Deleting model 'Press'
        db.delete_table('press_press')

        # Removing M2M table for field artists on 'Press'
        db.delete_table('press_press_artists')


    models = {
        'artists.artist': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Artist'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'resume': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('libs.slugify.fields.SlugifyField', [], {'max_length': '251', 'populate_from': "('first_name', 'last_name')"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'exhibitions.exhibition': {
            'Meta': {'ordering': "['-start_date']", 'object_name': 'Exhibition'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'exhibitions'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['artists.Artist']"}),
            'current': ('libs.unique_boolean.fields.UniqueBooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'press_release_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('libs.slugify.fields.SlugifyField', [], {'unique': 'True', 'max_length': '251', 'populate_from': "('get_year', 'name')"}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'photos.photo': {
            'Meta': {'ordering': "['position']", 'object_name': 'Photo'},
            'caption': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1000'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'})
        },
        'press.press': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Press'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'press'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['artists.Artist']"}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_file': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'exhibition': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'press'", 'null': 'True', 'to': "orm['exhibitions.Exhibition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'slug': ('libs.slugify.fields.SlugifyField', [], {'unique': 'True', 'max_length': '251', 'populate_from': "('get_year', 'publisher', 'title')"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['press']