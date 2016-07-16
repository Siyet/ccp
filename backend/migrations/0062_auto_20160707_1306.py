# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0061_auto_20160702_2354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuff',
            name='type',
            field=models.ForeignKey(related_name='type_cuffs', verbose_name='\u0422\u0438\u043f', to='dictionaries.CuffType'),
        ),
        migrations.AlterField(
            model_name='shirt',
            name='sleeve',
            field=models.ForeignKey(related_name='sleeve_shirts', default=2, verbose_name='\u0420\u0443\u043a\u0430\u0432', to='dictionaries.SleeveType'),
        ),
    ]
