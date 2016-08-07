# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import dictionaries.models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0071_auto_20160806_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shirt',
            name='sleeve',
            field=models.ForeignKey(related_name='sleeve_shirts', default=dictionaries.models.ResolveDefault(dictionaries.models.SleeveType), verbose_name='\u0420\u0443\u043a\u0430\u0432', to='dictionaries.SleeveType'),
        ),
    ]
