# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-07 05:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0015_fabrictype'),
        ('backend', '0039_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='fabric',
            name='fabric_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fabrics', to='dictionaries.FabricType', verbose_name='\u0422\u0438\u043f'),
        ),
    ]
