# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0002_auto_20160113_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cufftype',
            name='rounding',
            field=models.ManyToManyField(to='dictionaries.CuffRounding', verbose_name='\u0412\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u044f', blank=True),
        ),
    ]
