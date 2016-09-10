# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import processing.storage
import processing.upload_path


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0008_auto_20160909_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='composesource',
            name='shadow',
            field=models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/shadow/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0422\u0435\u043d\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='composesource',
            name='ao',
            field=models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/ao/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='AO', blank=True),
        ),
    ]
