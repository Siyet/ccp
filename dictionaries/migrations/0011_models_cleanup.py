# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0010_auto_20161211_1805'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shirtinfo',
            options={'verbose_name': '\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043e \u0441\u043e\u0440\u043e\u0447\u043a\u0430\u0445', 'verbose_name_plural': '\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043e \u0441\u043e\u0440\u043e\u0447\u043a\u0430\u0445'},
        ),
        migrations.AlterModelOptions(
            name='size',
            options={'ordering': ('order',), 'verbose_name': '\u0420\u0430\u0437\u043c\u0435\u0440 \u0441\u043e\u0440\u043e\u0447\u043a\u0438', 'verbose_name_plural': '\u0420\u0430\u0437\u043c\u0435\u0440\u044b \u0441\u043e\u0440\u043e\u0447\u0435\u043a'},
        ),
        migrations.DeleteModel(
            name='FAQ',
        ),
        migrations.RemoveField(
            model_name='shirtinfoimage',
            name='shirt_info',
        ),
        migrations.DeleteModel(
            name='ShirtInfoImage',
        ),
        migrations.DeleteModel(
            name='ShirtInfo',
        ),
    ]
