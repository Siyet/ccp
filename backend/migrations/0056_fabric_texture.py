# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-16 13:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0007_auto_20160611_1149'),
        ('backend', '0055_auto_20160616_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='fabric',
            name='texture',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fabric', to='processing.Texture', verbose_name='\u0422\u0435\u043a\u0441\u0442\u0443\u0440\u0430'),
        ),
    ]
