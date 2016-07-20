# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import processing.storage
import processing.upload_path


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0025_auto_20160717_2023'),
    ]

    operations = [
        migrations.CreateModel(
            name='StitchesSourceCache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_field', models.CharField(max_length=10)),
                ('pos_repr', models.CommaSeparatedIntegerField(max_length=20)),
                ('file', models.FileField(storage=processing.storage.OverwriteStorage(), upload_to=processing.upload_path.UploadComposeCache(b'composecache/%s/%s'))),
                ('source', models.ForeignKey(related_name='cache', to='processing.StitchesSource')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='stitchessourcecache',
            unique_together=set([('source', 'source_field')]),
        ),
    ]
