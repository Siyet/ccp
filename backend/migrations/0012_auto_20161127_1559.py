# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_auto_20161016_1916'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fabricresidual',
            options={'ordering': ['fabric'], 'verbose_name': '\u041e\u0441\u0442\u0430\u0442\u043e\u043a \u0442\u043a\u0430\u043d\u0438', 'verbose_name_plural': '\u041e\u0441\u0442\u0430\u0442\u043a\u0438 \u0442\u043a\u0430\u043d\u0435\u0439'},
        ),
    ]
