# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0006_remove_models_FAKE'),
        ('dictionaries', '0004_delete_fit'),
        ('female_configs', '0002_auto_20160904_2008'),
    ]

    operations = [
        migrations.CreateModel(
            name='FemaleBodySource',
            fields=[
                ('composesource_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='processing.ComposeSource')),
                ('back', models.ForeignKey(verbose_name='\u0421\u043f\u0438\u043d\u043a\u0430', blank=True, to='dictionaries.BackType', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('processing.composesource',),
        ),
    ]
