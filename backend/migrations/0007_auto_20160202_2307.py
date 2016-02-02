# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0007_size_sizeoptions'),
        ('backend', '0006_auto_20160202_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='shirt',
            name='size_option',
            field=models.ForeignKey(default=None, verbose_name='\u0412\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0439 \u0432\u0430\u0440\u0438\u0430\u043d\u0442 \u0440\u0430\u0437\u043c\u0435\u0440\u0430', to='dictionaries.SizeOptions'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shirt',
            name='size',
            field=models.ForeignKey(verbose_name='\u0420\u0430\u0437\u043c\u0435\u0440', blank=True, to='dictionaries.Size', null=True),
        ),
    ]
