# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-21 07:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0017_thickness'),
        ('backend', '0043_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='fabric',
            name='thickness',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fabrics', to='dictionaries.Thickness', verbose_name='\u0422\u043e\u043b\u0449\u0438\u043d\u0430'),
        ),
    ]
