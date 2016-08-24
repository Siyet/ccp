# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def populate_tuck(apps, scheme_editor):
    BackConfiguration = apps.get_model('processing', 'BackConfiguration')
    TuckType = apps.get_model('dictionaries', 'TuckType')
    no_tucks = TuckType.objects.get(title=u'Без вытачки')
    tucks = TuckType.objects.get(title=u'Вытачки')

    BackConfiguration.objects.filter(tuck=False).update(tucks=no_tucks.id)
    BackConfiguration.objects.filter(tuck=True).update(tucks=tucks.id)


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0001_initial'),
        ('dictionaries', '0002_tucktype')
    ]

    operations = [
        migrations.AddField(
            model_name='backconfiguration',
            name='tucks',
            field=models.IntegerField(default=0, verbose_name='\u0412\u044b\u0442\u0430\u0447\u043a\u0438'),
            preserve_default=False,
        ),
        migrations.RunPython(populate_tuck),
        migrations.AlterUniqueTogether(
            name='backconfiguration',
            unique_together=set([('back', 'hem', 'tucks')]),
        ),
        migrations.RemoveField(
            model_name='backconfiguration',
            name='tuck',
        ),
    ]
