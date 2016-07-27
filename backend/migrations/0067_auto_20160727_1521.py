# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0066_auto_20160720_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuff',
            name='rounding',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'types', chained_field=b'type', verbose_name='\u0422\u0438\u043f \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u044f', blank=True, to='dictionaries.CuffRounding', null=True),
        ),
    ]
