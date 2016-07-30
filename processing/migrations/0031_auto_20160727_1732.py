# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0030_auto_20160727_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stitchcolor',
            name='buttons_type',
            field=models.ForeignKey(verbose_name='\u041e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0430', to='backend.ElementStitch'),
        ),
    ]
