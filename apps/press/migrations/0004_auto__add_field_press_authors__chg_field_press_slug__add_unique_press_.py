# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Press.author'
        db.add_column(u'press_press', 'author',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True),
                      keep_default=False)


        # Changing field 'Press.slug'
        db.alter_column(u'press_press', 'slug', self.gf('libs.slugify.fields.SlugifyField')(unique=True, max_length=251, populate_from=('date_year', 'slug_title')))
        # Adding unique constraint on 'Press', fields ['publisher', 'title', 'artist', 'exhibition']
        db.create_unique(u'press_press', ['publisher', 'title', 'artist_id', 'exhibition_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Press', fields ['publisher', 'title', 'artist', 'exhibition']
        db.delete_unique(u'press_press', ['publisher', 'title', 'artist_id', 'exhibition_id'])

        # Deleting field 'Press.author'
        db.delete_column(u'press_press', 'author')


        # Changing field 'Press.slug'
        db.alter_column(u'press_press', 'slug', self.gf('libs.slugify.fields.SlugifyField')(max_length=251, unique=True, populate_from=('date_year', '__unicode__')))

    models = {
        u'artists.artist': {
            'Meta': {'ordering': "['-visible', 'last_name', 'first_name']", 'unique_together': "(('first_name', 'last_name'),)", 'object_name': 'Artist'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'resume': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('libs.slugify.fields.SlugifyField', [], {'max_length': '251', 'populate_from': "('first_name', 'last_name')"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'exhibitions.exhibition': {
            'Meta': {'ordering': "['-start_date']", 'object_name': 'Exhibition'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'exhibitions'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['artists.Artist']"}),
            'current': ('libs.unique_boolean.fields.UniqueBooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'extra_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'press_release_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'press_release_photo_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'press_release_photo_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('libs.slugify.fields.SlugifyField', [], {'unique': 'True', 'max_length': '251', 'populate_from': "('get_year', 'name')"}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        u'press.press': {
            'Meta': {'ordering': "['-date']", 'unique_together': "(('publisher', 'title', 'artist', 'exhibition'),)", 'object_name': 'Press'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'press'", 'null': 'True', 'to': u"orm['artists.Artist']"}),
            'author_first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'author_last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_file': ('django.db.models.fields.files.FileField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_text': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'exhibition': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'press'", 'null': 'True', 'to': u"orm['exhibitions.Exhibition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pages_range': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'slug': ('libs.slugify.fields.SlugifyField', [], {'unique': 'True', 'max_length': '251', 'populate_from': "('date_year', 'slug_title')"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'})
        }
    }

    complete_apps = ['press']
