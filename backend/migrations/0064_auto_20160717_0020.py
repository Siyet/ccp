# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0063_auto_20160716_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dickey',
            name='fabric',
            field=models.ForeignKey(related_name='dickey_list', verbose_name='\u0422\u043a\u0430\u043d\u044c', to='backend.Fabric'),
        ),
        migrations.AlterField(
            model_name='dickey',
            name='shirt',
            field=models.OneToOneField(related_name='dickey', to='backend.Shirt'),
        ),
        migrations.AlterField(
            model_name='dickey',
            name='type',
            field=models.ForeignKey(verbose_name='\u0422\u0438\u043f', to='dictionaries.DickeyType'),
        ),
    ]
