# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0007_discount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shop',
            options={'ordering': ('order',), 'verbose_name': '\u041c\u0430\u0433\u0430\u0437\u0438\u043d', 'verbose_name_plural': '\u041c\u0430\u0433\u0430\u0437\u0438\u043d\u044b'},
        ),
        migrations.AddField(
            model_name='shop',
            name='order',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='checkout_shop',
            field=models.ForeignKey(related_name='orders', verbose_name='\u041c\u0430\u0433\u0430\u0437\u0438\u043d', blank=True, to='checkout.Shop', null=True),
        ),
    ]
