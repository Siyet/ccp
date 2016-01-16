# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0004_fabriccategory'),
        ('backend', '0004_auto_20160116_1003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fabricprice',
            name='fabric',
        ),
        migrations.AddField(
            model_name='fabricprice',
            name='fabric_category',
            field=models.ForeignKey(related_name='prices', default=1, verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f \u0442\u043a\u0430\u043d\u0435\u0439', to='dictionaries.FabricCategory'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='storehouse',
            name='collection',
        ),
        migrations.AddField(
            model_name='storehouse',
            name='collection',
            field=models.ManyToManyField(to='backend.Collection', verbose_name='\u041a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u044f'),
        ),
        migrations.AlterUniqueTogether(
            name='fabricresidual',
            unique_together=set([('fabric', 'storehouse')]),
        ),
    ]
