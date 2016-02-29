# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-29 20:12
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0013_auto_20160229_2312'),
        ('backend', '0015_auto_20160229_2115'),
    ]

    operations = [
        migrations.AddField(
            model_name='collar',
            name='size',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field=b'type', chained_model_field=b'types', null=True, on_delete=django.db.models.deletion.CASCADE, to='dictionaries.CollarButtons', verbose_name='\u041f\u0443\u0433\u043e\u0432\u0438\u0446\u044b'),
        ),
        migrations.AddField(
            model_name='cuff',
            name='rounding',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field=b'type', chained_model_field=b'types', null=True, on_delete=django.db.models.deletion.CASCADE, to='dictionaries.CuffRounding', verbose_name='\u0422\u0438\u043f \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u044f'),
        ),
    ]
