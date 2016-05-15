# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-28 01:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0049_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shirt',
            name='code',
            field=models.CharField(max_length=255, null=True, verbose_name='\u0410\u0440\u0442\u0438\u043a\u0443\u043b'),
        ),
        migrations.AlterField(
            model_name='shirt',
            name='fabric',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.Fabric', verbose_name='\u0422\u043a\u0430\u043d\u044c'),
        ),
        migrations.AlterField(
            model_name='shirt',
            name='individualization',
            field=models.TextField(null=True, verbose_name='\u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044f'),
        ),
    ]