# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0008_auto_20160202_2312'),
        ('backend', '0007_auto_20160202_2307'),
    ]

    operations = [
        migrations.AddField(
            model_name='fabric',
            name='category',
            field=models.ForeignKey(related_name='fabrics', verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f', blank=True, to='dictionaries.FabricCategory', null=True),
        ),
    ]
