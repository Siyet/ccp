# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0013_auto_20180201_2300'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShirtInfo',
        ),
    ]
