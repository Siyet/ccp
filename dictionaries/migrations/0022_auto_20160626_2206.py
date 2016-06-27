# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0021_auto_20160626_2147'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='collartype',
            options={'ordering': ('order',), 'verbose_name': '\u0422\u0438\u043f \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430', 'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u043e\u0432'},
        ),
    ]
