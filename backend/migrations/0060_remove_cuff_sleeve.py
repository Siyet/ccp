# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0059_shirt_sleeve'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuff',
            name='sleeve',
        ),
    ]
