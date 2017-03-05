# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0007_auto_20161211_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='extra',
            field=models.CharField(max_length=255, verbose_name='\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u043e', blank=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='extra_en',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u043e', blank=True),
        ),
        migrations.AddField(
            model_name='shop',
            name='extra_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u043e', blank=True),
        ),
    ]
