# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0032_fabriccolor_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fabriccolor',
            options={'ordering': ('order',), 'verbose_name': '\u0426\u0432\u0435\u0442 \u0442\u043a\u0430\u043d\u0438', 'verbose_name_plural': '\u0426\u0432\u0435\u0442\u0430 \u0442\u043a\u0430\u043d\u0435\u0439'},
        ),
    ]
