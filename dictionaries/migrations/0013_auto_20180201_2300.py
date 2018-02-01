# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0012_delete_faq'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shirtinfoimage',
            name='shirt_info',
        ),
        migrations.DeleteModel(
            name='ShirtInfoImage',
        ),
    ]
