# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import processing.storage
import processing.upload_path


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0023_auto_20160713_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='composesource',
            name='ao',
            field=models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/ao/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0422\u0435\u043d\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='composesource',
            name='light',
            field=models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/light/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0421\u0432\u0435\u0442', blank=True),
        ),
    ]
