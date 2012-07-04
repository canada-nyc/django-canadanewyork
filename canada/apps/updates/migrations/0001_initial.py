# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Update'
        db.create_table('updates_update', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('exhibition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exhibitions.Exhibition'], blank=True)),
            ('post_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, blank=True)),
        ))
        db.send_create_signal('updates', ['Update'])

        # Adding M2M table for field artists on 'Update'
        db.create_table('updates_update_artists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('update', models.ForeignKey(orm['updates.update'], null=False)),
            ('artist', models.ForeignKey(orm['artists.artist'], null=False))
        ))
        db.create_unique('updates_update_artists', ['update_id', 'artist_id'])

        # Adding model 'UpdatePhoto'
        db.create_table('updates_updatephoto', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('update', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['updates.Update'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('updates', ['UpdatePhoto'])


    def backwards(self, orm):
        
        # Deleting model 'Update'
        db.delete_table('updates_update')

        # Removing M2M table for field artists on 'Update'
        db.delete_table('updates_update_artists')

        # Deleting model 'UpdatePhoto'
        db.delete_table('updates_updatephoto')


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
        'updates.update': {
            'Meta': {'ordering': "['-post_date']", 'object_name': 'Update'},
            'artists': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['artists.Artist']", 'symmetrical': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'exhibition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exhibitions.Exhibition']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'})
        },
        'updates.updatephoto': {
            'Meta': {'ordering': "['position']", 'object_name': 'UpdatePhoto'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'update': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['updates.Update']"})
        }
    }

    complete_apps = ['updates']
