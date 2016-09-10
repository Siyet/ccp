# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('male_configs', '0002_auto_20160904_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='malebodyconfiguration',
            name='cuff_types',
            field=models.ManyToManyField(to='dictionaries.CuffType', verbose_name='\u0422\u0438\u043f\u044b \u043c\u0430\u043d\u0436\u0435\u0442', blank=True),
        ),
    ]
