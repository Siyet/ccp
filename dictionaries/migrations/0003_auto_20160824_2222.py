# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0002_tucktype'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tucktype',
            options={'ordering': ('order',), 'verbose_name': '\u0422\u0438\u043f \u0432\u044b\u0442\u0430\u0447\u0435\u043a', 'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0432\u044b\u0442\u0430\u0447\u0435\u043a'},
        ),
        migrations.AlterField(
            model_name='tucktype',
            name='title',
            field=models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='tucktype',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
    ]
