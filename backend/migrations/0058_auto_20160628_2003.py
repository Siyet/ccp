# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0057_auto_20160626_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='custombuttons',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='hardness',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='shawloptions',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='shirt',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='stays',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
    ]
