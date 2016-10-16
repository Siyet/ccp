# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0010_collection_about_shirt_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fit',
            name='title',
            field=models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='shirt',
            name='fit',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'collections', chained_field=b'collection', verbose_name='\u0422\u0430\u043b\u0438\u044f', blank=True, to='backend.Fit', null=True),
        ),
    ]
