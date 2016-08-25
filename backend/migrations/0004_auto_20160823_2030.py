# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields


def populate_tuck(apps, scheme_editor):
    Shirt = apps.get_model('backend', 'Shirt')
    TuckType = apps.get_model('dictionaries', 'TuckType')
    no_tucks = TuckType.objects.get(title=u'Без вытачки')
    tucks = TuckType.objects.get(title=u'Вытачки')

    Shirt.objects.filter(tuck=False).update(tucks=no_tucks.id)
    Shirt.objects.filter(tuck=True).update(tucks=tucks.id)


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0002_tucktype'),
        ('backend', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='tuck',
            field=models.ManyToManyField(to='dictionaries.TuckType', verbose_name='\u0412\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u0432\u044b\u0442\u0430\u0447\u0435\u043a'),
        ),
        migrations.AddField(
            model_name='shirt',
            name='tucks',
            field=models.IntegerField(default=0, verbose_name='\u0412\u044b\u0442\u0430\u0447\u043a\u0438'),
            preserve_default=False,
        ),
        migrations.RunPython(populate_tuck),
        migrations.RemoveField(
            model_name='shirt',
            name='tuck',
        ),
    ]
