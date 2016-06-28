# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0022_auto_20160626_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backtype',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='collarbuttons',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='collartype',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='cufftype',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='dickeytype',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='fabricdesign',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='fabrictype',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='hemtype',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='plackettype',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='pockettype',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='size',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='sizeoptions',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='sleevetype',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='thickness',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='yoketype',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
    ]
