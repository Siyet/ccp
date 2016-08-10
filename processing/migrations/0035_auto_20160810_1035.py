# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0034_auto_20160731_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='sourcecache',
            name='resolution',
            field=models.CharField(default=b'preview', max_length=10, choices=[(b'full', b'full'), (b'preview', b'preview')]),
        ),
        migrations.AlterUniqueTogether(
            name='sourcecache',
            unique_together=set([('content_type', 'object_id', 'source_field', 'resolution')]),
        ),
    ]
