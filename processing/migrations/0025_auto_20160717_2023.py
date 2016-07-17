# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0024_auto_20160717_1800'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stitchessource',
            unique_together=set([('content_type', 'object_id', 'projection', 'type')]),
        ),
    ]
