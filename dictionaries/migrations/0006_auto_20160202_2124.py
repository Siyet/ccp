# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0005_shirtinfo_shirtinfoimage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shirtinfo',
            options={'verbose_name': '\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043e \u0440\u0443\u0431\u0430\u0448\u043a\u0430\u0445', 'verbose_name_plural': '\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043e \u0440\u0443\u0431\u0430\u0448\u043a\u0430\u0445'},
        ),
        migrations.AlterField(
            model_name='shirtinfoimage',
            name='text',
            field=models.TextField(verbose_name='\u0422\u0435\u043a\u0441\u0442 \u043f\u043e\u0434 \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435\u043c'),
        ),
    ]
