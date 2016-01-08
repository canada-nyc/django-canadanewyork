# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-08 13:28
from __future__ import unicode_literals

from django.db import migrations

from apps.photos.migrations.base_preset_order import preset_photo_order


class Migration(migrations.Migration):
    dependencies = [
        ('books', '0005_auto_20160104_1403'),
    ]

    operations = [
        migrations.RunPython(preset_photo_order(('books', 'BookPhoto')))
    ]
