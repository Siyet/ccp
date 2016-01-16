# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shirt',
            name='collar',
        ),
        migrations.RemoveField(
            model_name='shirt',
            name='cuffs',
        ),
        migrations.AddField(
            model_name='collar',
            name='shirt',
            field=models.OneToOneField(related_name='collar', default=1, to='backend.Shirt'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cuff',
            name='shirt',
            field=models.OneToOneField(related_name='cuff', default=1, to='backend.Shirt'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='shirt',
            name='size',
            field=models.IntegerField(blank=True, null=True, verbose_name='\u0420\u0430\u0437\u043c\u0435\u0440', choices=[(35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42)]),
        ),
    ]
