# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-04 04:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0048_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabric',
            name='long_description',
            field=models.TextField(blank=True, null=True, verbose_name='\u041f\u043e\u043b\u043d\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='short_description',
            field=models.TextField(blank=True, null=True, verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
        ),
    ]
