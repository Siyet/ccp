# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def set_initials_colors(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Color = apps.get_model("dictionaries", "Color")
    Color.objects.update(title=models.F('color'))


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0023_auto_20160628_2003'),
    ]

    operations = [
        migrations.RunPython(set_initials_colors),
    ]
