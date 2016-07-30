# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0032_auto_20160727_1955'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='texture',
            name='cache',
        ),
        migrations.RemoveField(
            model_name='texture',
            name='tiling',
        ),
    ]
