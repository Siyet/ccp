# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0026_auto_20160702_2354'),
        ('processing', '0018_auto_20160704_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuffbuttonssource',
            name='cuff',
            field=models.ForeignKey(related_name='cbs', null=True, verbose_name='\u0422\u0438\u043f \u043c\u0430\u0436\u0435\u0442\u044b', to='dictionaries.CuffType'),
        ),
        migrations.AddField(
            model_name='cuffbuttonssource',
            name='rounding_types',
            field=models.ManyToManyField(related_name='cbs', verbose_name='\u0422\u0438\u043f\u044b \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u044f', to='dictionaries.CuffRounding', blank=True),
        ),
    ]
