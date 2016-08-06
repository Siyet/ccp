# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import backend.models
import dictionaries.models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0070_auto_20160802_2031'),
        ('dictionaries', '0028_auto_20160806_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shirt',
            name='shawl',
            field=models.ForeignKey(default=dictionaries.models.ResolveDefault(backend.models.ShawlOptions), verbose_name='\u041f\u043b\u0430\u0442\u043e\u043a', to='backend.ShawlOptions', null=True),
        ),
    ]
