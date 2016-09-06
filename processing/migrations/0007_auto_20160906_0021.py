# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import processing.storage
import processing.upload_path


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0006_remove_models_FAKE'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuffconfiguration',
            name='side_mask',
            field=models.FileField(storage=processing.storage.OverwriteStorage(), upload_to=processing.upload_path.UploadComposingSource(b'composesource/%s/%s'), null=True, verbose_name='\u041c\u0430\u0441\u043a\u0430 \u0440\u0443\u043a\u0430\u0432\u0430 (\u0441\u0431\u043e\u043a\u0443)', blank=True),
        ),
    ]
