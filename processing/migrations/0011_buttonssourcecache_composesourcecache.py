# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields
import processing.upload_path
import processing.storage


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0010_auto_20160630_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='ButtonsSourceCache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_field', models.CharField(max_length=10)),
                ('bounding_box', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('file', models.FileField(storage=processing.storage.OverwriteStorage(), upload_to=processing.upload_path.UploadComposeCache(b'composecache/%s/%s'))),
                ('source', models.ForeignKey(to='processing.ButtonsSource')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ComposeSourceCache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_field', models.CharField(max_length=10)),
                ('bounding_box', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('file', models.FileField(storage=processing.storage.OverwriteStorage(), upload_to=processing.upload_path.UploadComposeCache(b'composecache/%s/%s'))),
                ('source', models.ForeignKey(to='processing.ComposeSource')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
