# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0031_auto_20160727_1732'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stitchcolor',
            old_name='buttons_type',
            new_name='element',
        ),
    ]
