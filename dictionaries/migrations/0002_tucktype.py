# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_tucks(apps, scheme_editor):
    Tuck = apps.get_model('dictionaries', 'tucktype')
    Tuck.objects.create(title=u'Без вытачки')
    Tuck.objects.create(title=u'Вытачки')


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TuckType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True, default=0)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u0432\u044b\u0442\u0430\u0447\u0435\u043a',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0432\u044b\u0442\u0430\u0447\u0435\u043a',
            },
        ),
        migrations.RunPython(create_tucks)
    ]
