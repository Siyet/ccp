# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-10 14:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0005_auto_20160610_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placketsource',
            name='placket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionaries.PlacketType', verbose_name='\u0422\u0438\u043f \u043f\u043e\u043b\u043e\u0447\u043a\u0438'),
        ),
    ]