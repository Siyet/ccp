# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def move_fit(apps, scheme_editor):
    Shirt = apps.get_model('backend', 'Shirt')
    Fit = apps.get_model('dictionaries', 'Fit')
    NewFit = apps.get_model('backend', 'Fit')
    new_fit_map = {}
    for ind, x in enumerate(Fit.objects.all()):
        new_fit = NewFit.objects.create(id=x.id, title=x.title, order=ind)
        new_fit_map[new_fit.id] = new_fit
    for shirt in Shirt.objects.filter(fit__isnull=False):
        shirt.new_fit = new_fit_map[shirt.fit.id]
        shirt.save()


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0003_auto_20160824_2222'),
        ('backend', '0005_auto_20160824_2222'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'fit', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
                ('collections', models.ManyToManyField(related_name='fits', verbose_name='\u041a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u0438', to='backend.Collection')),
                ('sizes', models.ManyToManyField(related_name='fits', verbose_name='\u0420\u0430\u0437\u043c\u0435\u0440\u044b', to='dictionaries.Size')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u0422\u0438\u043f \u0442\u0430\u043b\u0438\u0438',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0442\u0430\u043b\u0438\u0438',
            },
        ),
        migrations.AddField(
            model_name='shirt',
            name='new_fit',
            field=models.ForeignKey(verbose_name='\u0422\u0430\u043b\u0438\u044f', blank=True, to='backend.Fit', null=True),
        ),
        migrations.RunPython(move_fit),
    ]
