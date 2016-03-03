# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-02 00:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0016_auto_20160229_2312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storehouse',
            name='collection',
        ),
        migrations.AddField(
            model_name='collection',
            name='storehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='collections', to='backend.Storehouse', verbose_name='\u0421\u043a\u043b\u0430\u0434'),
        ),
    ]
