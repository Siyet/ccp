# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('female_configs', '0008_auto_20160911_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='femalebackshadow',
            name='back',
        ),
        migrations.DeleteModel(
            name='FemaleBackShadow',
        ),
    ]
