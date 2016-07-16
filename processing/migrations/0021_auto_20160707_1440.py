# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0020_auto_20160705_1428'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='buttonssourcecache',
            unique_together=set([('source', 'source_field')]),
        ),
        migrations.AlterUniqueTogether(
            name='composesourcecache',
            unique_together=set([('source', 'source_field')]),
        ),
    ]
