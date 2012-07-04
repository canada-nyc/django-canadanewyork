# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Press'
        db.create_table('press_press', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('publisher', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=60, blank=True)),
            ('exhibition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exhibitions.Exhibition'], null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, unique=True, max_length=50, blank=True)),
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
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'exhibitions.exhibition': {
            'Meta': {'ordering': "['-start_date']", 'object_name': 'Exhibition'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['artists.Artist']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'frontpage': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'frontpage_selected_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'frontpage_selected_image'", 'null': 'True', 'to': "orm['exhibitions.ExhibitionPhoto']"}),
            'frontpage_text': ('django.db.models.fields.TextField', [], {'max_length': '800', 'null': 'True', 'blank': 'True'}),
            'frontpage_uploaded_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'exhibitions.exhibitionphoto': {
            'Meta': {'ordering': "['position']", 'object_name': 'ExhibitionPhoto'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'exhibition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exhibitions.Exhibition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'press.press': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Press'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['artists.Artist']", 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'exhibition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exhibitions.Exhibition']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['press']
