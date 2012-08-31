# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Update.exhibition'
        db.delete_column('updates_update', 'exhibition_id')

        # Removing M2M table for field artists on 'Update'
        db.delete_table('updates_update_artists')


        # Changing field 'Update.post_date'
        db.alter_column('updates_update', 'post_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))
        # Deleting field 'UpdatePhoto.dimensions'
        db.delete_column('updates_updatephoto', 'dimensions')

        # Deleting field 'UpdatePhoto.year'
        db.delete_column('updates_updatephoto', 'year')

        # Deleting field 'UpdatePhoto.medium'
        db.delete_column('updates_updatephoto', 'medium')

        # Adding field 'UpdatePhoto.caption'
        db.add_column('updates_updatephoto', 'caption',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)


        # Changing field 'UpdatePhoto.title'
        db.alter_column('updates_updatephoto', 'title', self.gf('django.db.models.fields.CharField')(max_length=20))

    def backwards(self, orm):
        # Adding field 'Update.exhibition'
        db.add_column('updates_update', 'exhibition',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exhibitions.Exhibition'], null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field artists on 'Update'
        db.create_table('updates_update_artists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('update', models.ForeignKey(orm['updates.update'], null=False)),
            ('artist', models.ForeignKey(orm['artists.artist'], null=False))
        ))
        db.create_unique('updates_update_artists', ['update_id', 'artist_id'])


        # Changing field 'Update.post_date'
        db.alter_column('updates_update', 'post_date', self.gf('django.db.models.fields.DateTimeField')())
        # Adding field 'UpdatePhoto.dimensions'
        db.add_column('updates_updatephoto', 'dimensions',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True),
                      keep_default=False)

        # Adding field 'UpdatePhoto.year'
        db.add_column('updates_updatephoto', 'year',
                      self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'UpdatePhoto.medium'
        db.add_column('updates_updatephoto', 'medium',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Deleting field 'UpdatePhoto.caption'
        db.delete_column('updates_updatephoto', 'caption')


        # Changing field 'UpdatePhoto.title'
        db.alter_column('updates_updatephoto', 'title', self.gf('django.db.models.fields.CharField')(max_length=50))

    models = {
        'updates.update': {
            'Meta': {'ordering': "['-post_date']", 'object_name': 'Update'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        'updates.updatephoto': {
            'Meta': {'ordering': "['position']", 'object_name': 'UpdatePhoto'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'update': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['updates.Update']"})
        }
    }

    complete_apps = ['updates']