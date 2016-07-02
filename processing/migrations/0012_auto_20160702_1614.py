# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import processing.storage


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0011_buttonssourcecache_composesourcecache'),
    ]

    operations = [
        migrations.AddField(
            model_name='texture',
            name='cache',
            field=models.FileField(storage=processing.storage.OverwriteStorage(), upload_to=b'textures/cache', null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='composesourcecache',
            name='source',
            field=models.ForeignKey(related_name='cache', to='processing.ComposeSource'),
        ),
    ]
