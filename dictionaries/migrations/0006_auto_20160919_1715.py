# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0005_tucktype_picture'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='yoketype',
            options={'ordering': ('order',), 'verbose_name': '\u0422\u0438\u043f \u043a\u043e\u043a\u0435\u0442\u043a\u0438', 'verbose_name_plural': '\u0422\u0438\u043f\u044b \u043a\u043e\u043a\u0435\u0442\u043a\u0438'},
        ),
    ]
