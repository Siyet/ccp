# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-27 05:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0046_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fabric',
            old_name='description',
            new_name='short_description',
        ),
    ]