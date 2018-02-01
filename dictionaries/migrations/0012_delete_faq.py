# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0011_auto_20180131_2200'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FAQ',
        ),
    ]
