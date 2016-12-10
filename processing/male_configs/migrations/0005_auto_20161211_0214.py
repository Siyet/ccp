# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('male_configs', '0004_auto_20161210_1647'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='malebodybuttonsconfiguration',
            options={'verbose_name': 'body buttons configuration', 'verbose_name_plural': 'body buttons configurations'},
        ),
        migrations.AlterField(
            model_name='malebodysource',
            name='tuck',
            field=models.ForeignKey(default=None, blank=True, to='dictionaries.TuckType', null=True, verbose_name='\u0412\u044b\u0442\u0430\u0447\u043a\u0438'),
        ),
    ]
