# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0008_auto_20160202_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabriccategory',
            name='title',
            field=models.CharField(unique=True, max_length=1, verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f', db_index=True),
        ),
    ]
