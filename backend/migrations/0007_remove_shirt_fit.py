# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_auto_20160825_2122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shirt',
            name='fit',
        ),
        migrations.RenameField(
            model_name='shirt',
            old_name='new_fit',
            new_name='fit',
        ),
    ]
