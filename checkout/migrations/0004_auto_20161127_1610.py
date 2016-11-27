# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20161127_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='city_en',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0413\u043e\u0440\u043e\u0434'),
        ),
        migrations.AddField(
            model_name='shop',
            name='city_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0413\u043e\u0440\u043e\u0434'),
        ),
        migrations.AddField(
            model_name='shop',
            name='street_en',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0423\u043b\u0438\u0446\u0430'),
        ),
        migrations.AddField(
            model_name='shop',
            name='street_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0423\u043b\u0438\u0446\u0430'),
        ),
    ]
