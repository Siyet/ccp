# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0008_auto_20160626_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
    ]
