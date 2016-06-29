# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0013_auto_20160627_2126'),
        ('yandex_kassa', '0005_auto_20160109_0638')
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
