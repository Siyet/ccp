# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import processing.storage
import processing.upload_path


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0035_auto_20160810_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourcecache',
            name='file',
            field=models.FileField(storage=processing.storage.OverwriteStorage(), upload_to=processing.upload_path.UploadComposeCache(b'composecache/%s/%s/%s')),
        ),
    ]
