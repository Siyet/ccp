# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0003_auto_20160824_2222'),
        ('processing', '0002_auto_20160824_2116'),
    ]

    operations = [
        migrations.RenameField(
            model_name='backconfiguration',
            old_name='tucks',
            new_name='tuck'
        ),
        migrations.AlterField(
            model_name='backconfiguration',
            name='tuck',
            field=models.ForeignKey(verbose_name='\u0412\u044b\u0442\u0430\u0447\u043a\u0438', to='dictionaries.TuckType'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='backconfiguration',
            unique_together=set([('back', 'hem', 'tuck')]),
        ),
    ]
