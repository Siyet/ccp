# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-15 08:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_certificate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certificate',
            name='spent',
        ),
    ]