# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-16 19:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_auto_20160216_2209'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='templateshirt',
            options={'verbose_name': '\u0428\u0430\u0431\u043b\u043e\u043d \u0440\u0443\u0431\u0430\u0448\u043a\u0438', 'verbose_name_plural': '\u0428\u0430\u0431\u043b\u043e\u043d\u044b \u0440\u0443\u0431\u0430\u0448\u0435\u043a'},
        ),
        migrations.AddField(
            model_name='shirt',
            name='description',
            field=models.TextField(default='', verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shirt',
            name='individualization',
            field=models.TextField(default='', verbose_name='\u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044f'),
            preserve_default=False,
        ),
    ]
