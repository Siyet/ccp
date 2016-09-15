# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0004_delete_fit'),
    ]

    operations = [
        migrations.AddField(
            model_name='tucktype',
            name='picture',
            field=models.ImageField(default='', upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435'),
            preserve_default=False,
        ),
    ]
