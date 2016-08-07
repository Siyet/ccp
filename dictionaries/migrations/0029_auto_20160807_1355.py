# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0028_auto_20160806_1259'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='defaultelement',
            unique_together=set([]),
        ),
    ]
