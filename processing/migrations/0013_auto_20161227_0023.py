# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0012_auto_20161211_0226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='texture',
            name='moire_filter',
        ),
        migrations.AddField(
            model_name='texture',
            name='gamma_correction',
            field=models.BooleanField(default=False, verbose_name='\u0413\u0430\u043c\u043c\u0430-\u043a\u043e\u0440\u0440\u0435\u043a\u0446\u0438\u044f'),
        ),
    ]
