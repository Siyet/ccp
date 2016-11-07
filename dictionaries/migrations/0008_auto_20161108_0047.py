# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0007_fabriccolor_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='color',
            options={'ordering': ('order',), 'verbose_name': '\u0426\u0432\u0435\u0442 (\u0434\u043b\u044f \u0438\u043d\u0438\u0446\u0438\u0430\u043b\u043e\u0432)', 'verbose_name_plural': '\u0426\u0432\u0435\u0442\u0430 (\u0434\u043b\u044f \u0438\u043d\u0438\u0446\u0438\u0430\u043b\u043e\u0432)'},
        ),
        migrations.AlterModelOptions(
            name='stitchcolor',
            options={'ordering': ('order',), 'verbose_name': '\u0426\u0432\u0435\u0442 \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438', 'verbose_name_plural': '\u0426\u0432\u0435\u0442\u0430 \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438'},
        ),
        migrations.AddField(
            model_name='color',
            name='order',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stitchcolor',
            name='order',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=False,
        ),
    ]
