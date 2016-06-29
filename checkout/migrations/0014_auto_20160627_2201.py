# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yandex_kassa', '0006_auto_20160627_2201'),
        ('checkout', '0013_auto_20160627_2126'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.OneToOneField(null=True, blank=True, to='yandex_kassa.Payment'),
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
