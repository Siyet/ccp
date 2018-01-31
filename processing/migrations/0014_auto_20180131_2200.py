# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0013_auto_20161227_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodybuttonsconfiguration',
            name='sex',
            field=models.CharField(default=b'male', max_length=10, choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'), (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f')]),
        ),
        migrations.AlterField(
            model_name='cuffbuttonsconfiguration',
            name='sex',
            field=models.CharField(default=b'male', max_length=10, choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'), (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f')]),
        ),
        migrations.AlterField(
            model_name='cuffconfiguration',
            name='sex',
            field=models.CharField(default=b'male', max_length=10, choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'), (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f')]),
        ),
        migrations.AlterField(
            model_name='initialsconfiguration',
            name='sex',
            field=models.CharField(default=b'male', max_length=10, choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'), (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f')]),
        ),
        migrations.AlterField(
            model_name='pocketconfiguration',
            name='sex',
            field=models.CharField(default=b'male', max_length=10, choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'), (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f')]),
        ),
        migrations.AlterField(
            model_name='yokeconfiguration',
            name='sex',
            field=models.CharField(default=b'male', max_length=10, choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'), (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f')]),
        ),
    ]
