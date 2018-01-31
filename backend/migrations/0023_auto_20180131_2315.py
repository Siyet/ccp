# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0022_auto_20180131_2311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='text',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='text_en',
        ),
        migrations.RemoveField(
            model_name='collection',
            name='text_ru',
        ),
    ]
