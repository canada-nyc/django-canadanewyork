# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Exhibition'
        db.create_table('exhibitions_exhibition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('frontpage', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('frontpage_uploaded_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('frontpage_selected_image', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='frontpage_selected_image', null=True, to=orm['exhibitions.ExhibitionPhoto'])),
            ('frontpage_text', self.gf('django.db.models.fields.TextField')(max_length=800, null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('end_date', self.gf('django.db.models.fields.DateField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, blank=True)),
        ))
        db.send_create_signal('exhibitions', ['Exhibition'])

        # Adding M2M table for field artists on 'Exhibition'
        db.create_table('exhibitions_exhibition_artists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('exhibition', models.ForeignKey(orm['exhibitions.exhibition'], null=False)),
            ('artist', models.ForeignKey(orm['artists.artist'], null=False))
        ))
        db.create_unique('exhibitions_exhibition_artists', ['exhibition_id', 'artist_id'])

        # Adding model 'ExhibitionPhoto'
        db.create_table('exhibitions_exhibitionphoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exhibition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exhibitions.Exhibition'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('exhibitions', ['ExhibitionPhoto'])


    def backwards(self, orm):
        
        # Deleting model 'Exhibition'
        db.delete_table('exhibitions_exhibition')

        # Removing M2M table for field artists on 'Exhibition'
        db.delete_table('exhibitions_exhibition_artists')

        # Deleting model 'ExhibitionPhoto'
        db.delete_table('exhibitions_exhibitionphoto')


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
        }
    }

    complete_apps = ['exhibitions']
