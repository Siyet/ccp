# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0007_size_sizeoptions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sizeoptions',
            old_name='show_options',
            new_name='show_sizes',
        ),
    ]
