# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0077_auto_20160818_1750'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fabric',
            old_name='fabric_type',
            new_name='type',
        ),
    ]
