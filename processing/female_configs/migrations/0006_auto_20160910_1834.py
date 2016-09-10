# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('female_configs', '0005_auto_20160910_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='femalecollarbuttonsconfiguration',
            name='buttons',
            field=models.IntegerField(default=1, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u0443\u0433\u043e\u0432\u0438\u0446', choices=[(0, 0), (1, 1), (2, 2)]),
        ),
        migrations.AlterField(
            model_name='femalebodyconfiguration',
            name='cuff_types',
            field=models.ManyToManyField(to='dictionaries.CuffType', verbose_name='\u0422\u0438\u043f\u044b \u043c\u0430\u043d\u0436\u0435\u0442', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='femalecollarbuttonsconfiguration',
            unique_together=set([('collar', 'buttons')]),
        ),
    ]
