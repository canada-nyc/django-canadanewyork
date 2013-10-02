# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Book.month'
        db.delete_column(u'books_book', 'month')

        # Deleting field 'Book.year'
        db.delete_column(u'books_book', 'year')

        # Adding field 'Book.date'
        db.add_column(u'books_book', 'date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 10, 2, 0, 0)),
                      keep_default=False)

        # Adding field 'Book.date_text'
        db.add_column(u'books_book', 'date_text',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Book.month'
        db.add_column(u'books_book', 'month',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'Book.year'
        db.add_column(u'books_book', 'year',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=datetime.datetime(2013, 10, 2, 0, 0)),
                      keep_default=False)

        # Deleting field 'Book.date'
        db.delete_column(u'books_book', 'date')

        # Deleting field 'Book.date_text'
        db.delete_column(u'books_book', 'date_text')


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
        u'books.book': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Book'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'books'", 'to': u"orm['artists.Artist']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'date_text': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        }
    }

    complete_apps = ['books']