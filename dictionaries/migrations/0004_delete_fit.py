# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0003_auto_20160824_2222'),
        ('backend', '0007_remove_shirt_fit'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Fit',
        ),
    ]
