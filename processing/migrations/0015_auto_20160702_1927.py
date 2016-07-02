# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0014_generic_related_sources'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='composesource',
            name='back_source',
        ),
        migrations.RemoveField(
            model_name='composesource',
            name='body_source',
        ),
        migrations.RemoveField(
            model_name='composesource',
            name='collar_source',
        ),
        migrations.RemoveField(
            model_name='composesource',
            name='cuff_source',
        ),
        migrations.RemoveField(
            model_name='composesource',
            name='placket_source',
        ),
        migrations.RemoveField(
            model_name='composesource',
            name='pocket_source',
        ),
        migrations.RemoveField(
            model_name='buttonssource',
            name='body_buttons',
        ),
        migrations.RemoveField(
            model_name='buttonssource',
            name='cuff_buttons',
        ),
        migrations.RemoveField(
            model_name='buttonssource',
            name='collar_buttons',
        ),
    ]
