# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0003_auto_20160824_2222'),
        ('backend', '0004_auto_20160823_2030'),
    ]

    operations = [
         migrations.RenameField(
            model_name='shirt',
            old_name='tucks',
            new_name='tuck'
        ),
        migrations.AlterField(
            model_name='shirt',
            name='tuck',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'collections', chained_field=b'collection', verbose_name='\u0412\u044b\u0442\u0430\u0447\u043a\u0438', show_all=True, to='dictionaries.TuckType'),
            preserve_default=False
        )
    ]
