# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-20 05:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0041_auto_20160420_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shirt',
            name='yoke',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dictionaries.YokeType', verbose_name='\u041a\u043e\u043a\u0435\u0442\u043a\u0430'),
        ),
    ]
