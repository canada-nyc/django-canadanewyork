# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-22 11:11
from __future__ import unicode_literals

from django.db import migrations, models
import libs.ckeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(db_index=True, max_length=100)),
                ('content', libs.ckeditor.fields.CKEditorField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'custom pages',
                'verbose_name': 'custom page',
                'ordering': ('path',),
            },
        ),
    ]
