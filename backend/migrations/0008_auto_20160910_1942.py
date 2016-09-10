# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_remove_shirt_fit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='tuck',
            field=models.ManyToManyField(related_name='collections', verbose_name='\u0412\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u0432\u044b\u0442\u0430\u0447\u0435\u043a', to='dictionaries.TuckType'),
        ),
    ]
