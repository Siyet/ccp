# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0010_auto_20160912_1727'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CollarConfiguration',
        ),
    ]
