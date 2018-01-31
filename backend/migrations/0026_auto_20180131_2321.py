# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0025_collection_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='image',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='text',
        ),
    ]
