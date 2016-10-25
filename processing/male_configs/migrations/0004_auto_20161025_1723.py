# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('male_configs', '0003_auto_20160910_1834'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='malebackconfiguration',
            unique_together=set([('back', 'tuck')]),
        ),
        migrations.RemoveField(
            model_name='malebackconfiguration',
            name='hem',
        ),
    ]
