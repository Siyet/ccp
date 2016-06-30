# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yandex_kassa', '0005_auto_20160109_0638'),
        ('checkout', '0015_auto_20160629_2157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': '\u041f\u043b\u0430\u0442\u0435\u0436',
                'proxy': True,
                'verbose_name_plural': '\u041f\u043b\u0430\u0442\u0435\u0436\u0438',
            },
            bases=('yandex_kassa.payment',),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.OneToOneField(related_name='order', null=True, blank=True, to='checkout.Payment'),
        ),
    ]
