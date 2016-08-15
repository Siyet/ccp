# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0030_fit_sleevelength'),
    ]

    operations = [
        migrations.AddField(
            model_name='plackettype',
            name='show_buttons',
            field=models.BooleanField(default=True, verbose_name='\u041f\u0443\u0433\u043e\u0432\u0438\u0446\u044b \u0432\u0438\u0434\u043d\u044b'),
        ),
    ]
