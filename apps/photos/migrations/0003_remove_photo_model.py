# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Photo'
        db.delete_table(u'photos_photo')


    def backwards(self, orm):
        # Adding model 'Photo'
        db.create_table(u'photos_photo', (
            ('thumbnail_image_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('medium', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('large_image', self.gf('django.db.models.fields.files.ImageField')(max_length=1000, null=True, blank=True)),
            ('thumbnail_image_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=400, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=1000)),
            ('width', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('large_image_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('height', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('caption', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('depth', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=6, decimal_places=2, blank=True)),
            ('thumbnail_image', self.gf('django.db.models.fields.files.ImageField')(max_length=1000, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('large_image_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('artist_text', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'photos', ['Photo'])


    models = {

    }

    depends_on = (
        ("artists", "0003_seperate_photos"),
        ("exhibitions", "0004_seperate_photos"),
        ("updates", "0003_seperate_photos"),
    )

    complete_apps = ['photos']
