# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import processing.storage
import processing.upload_path


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('processing', '0027_auto_20160718_1859'),
    ]

    operations = [
        migrations.CreateModel(
            name='SourceCache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_field', models.CharField(max_length=10)),
                ('pos_repr', models.CommaSeparatedIntegerField(max_length=20)),
                ('file', models.FileField(storage=processing.storage.OverwriteStorage(), upload_to=processing.upload_path.UploadComposeCache(b'composecache/%s/%s'))),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='buttonssourcecache',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='buttonssourcecache',
            name='source',
        ),
        migrations.AlterUniqueTogether(
            name='composesourcecache',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='composesourcecache',
            name='source',
        ),
        migrations.AlterUniqueTogether(
            name='stitchessourcecache',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='stitchessourcecache',
            name='source',
        ),
        migrations.DeleteModel(
            name='ButtonsSourceCache',
        ),
        migrations.DeleteModel(
            name='ComposeSourceCache',
        ),
        migrations.DeleteModel(
            name='StitchesSourceCache',
        ),
        migrations.AlterUniqueTogether(
            name='sourcecache',
            unique_together=set([('content_type', 'object_id', 'source_field')]),
        ),
    ]
