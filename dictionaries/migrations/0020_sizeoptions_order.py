# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0019_auto_20160519_1940'),
    ]

    operations = [
        migrations.AddField(
            model_name='sizeoptions',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
    ]
