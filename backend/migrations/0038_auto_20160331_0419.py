# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-31 01:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0037_auto_20160330_0721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storehouse',
            name='country',
            field=models.CharField(max_length=255, unique=True, verbose_name='\u0421\u0442\u0440\u0430\u043d\u0430'),
        ),
    ]