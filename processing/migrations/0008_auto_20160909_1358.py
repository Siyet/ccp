# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0007_auto_20160906_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pocketconfiguration',
            name='pocket',
            field=models.ForeignKey(verbose_name='\u0422\u0438\u043f \u043a\u0430\u0440\u043c\u0430\u043d\u0430', to='dictionaries.PocketType'),
        ),
        migrations.AlterUniqueTogether(
            name='pocketconfiguration',
            unique_together=set([('pocket', 'sex')]),
        ),
    ]
