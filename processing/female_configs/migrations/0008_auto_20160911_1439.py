# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('female_configs', '0007_auto_20160910_1942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='femalecollarbuttonsconfiguration',
            name='collar',
            field=models.ForeignKey(verbose_name='\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a', to='dictionaries.CollarType'),
        ),
    ]
