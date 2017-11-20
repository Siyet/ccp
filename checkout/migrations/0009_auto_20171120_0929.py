# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0008_auto_20170227_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerdata',
            name='email',
            field=models.EmailField(max_length=255, null=True, verbose_name='Email'),
        ),
    ]
