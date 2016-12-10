# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0009_auto_20161127_1610'),
        ('processing', '0011_delete_collarconfiguration'),
    ]

    operations = [
        migrations.AddField(
            model_name='bodybuttonsconfiguration',
            name='plackets',
            field=models.ManyToManyField(to='dictionaries.PlacketType', verbose_name='\u0422\u0438\u043f \u043f\u043e\u043b\u043e\u0447\u043a\u0438'),
        ),
        migrations.AlterUniqueTogether(
            name='bodybuttonsconfiguration',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='bodybuttonsconfiguration',
            name='buttons',
        ),
    ]
