# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processing', '0001_initial'),
        ('dictionaries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FemaleBodyConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cuff_types', models.ManyToManyField(to='dictionaries.CuffType', verbose_name='\u0422\u0438\u043f\u044b \u043c\u0430\u043d\u0436\u0435\u0442')),
                ('hem', models.ForeignKey(verbose_name='\u041d\u0438\u0437', to='dictionaries.HemType')),
                ('sleeve', models.ForeignKey(verbose_name='\u0420\u0443\u043a\u0430\u0432', to='dictionaries.SleeveType')),
                ('tuck', models.ForeignKey(verbose_name='\u0412\u044b\u0442\u0430\u0447\u043a\u0438', to='dictionaries.TuckType')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043e\u0441\u043d\u043e\u0432\u044b',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043e\u0441\u043d\u043e\u0432\u044b',
            },
        ),
        migrations.CreateModel(
            name='FemaleCollarButtonsConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collar', models.OneToOneField(verbose_name='\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a', to='dictionaries.CollarType')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043f\u0443\u0433\u043e\u0432\u0438\u0446 \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043f\u0443\u0433\u043e\u0432\u0438\u0446 \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
            },
        ),
        migrations.CreateModel(
            name='FemaleCollarConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collar', models.OneToOneField(verbose_name='\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a', to='dictionaries.CollarType')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
            },
        ),
        migrations.CreateModel(
            name='FemalePlacketConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hem', models.ForeignKey(verbose_name='\u041d\u0438\u0437', to='dictionaries.HemType')),
                ('plackets', models.ManyToManyField(to='dictionaries.PlacketType', verbose_name='\u0422\u0438\u043f \u043f\u043e\u043b\u043e\u0447\u043a\u0438')),
                ('tuck', models.ForeignKey(verbose_name='\u0412\u044b\u0442\u0430\u0447\u043a\u0438', to='dictionaries.TuckType')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043f\u043e\u043b\u043e\u0447\u043a\u0438',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043f\u043e\u043b\u043e\u0447\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='FemaleBodyButtonsConfiguration',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('processing.bodybuttonsconfiguration', models.Model),
        ),
        migrations.CreateModel(
            name='FemaleCuffButtonsConfiguration',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('processing.cuffbuttonsconfiguration', models.Model),
        ),
        migrations.CreateModel(
            name='FemaleCuffConfiguration',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('processing.cuffconfiguration',),
        ),
        migrations.CreateModel(
            name='FemaleInitialsConfiguration',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('processing.initialsconfiguration', models.Model),
        ),
        migrations.CreateModel(
            name='FemalePocketConfiguration',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('processing.pocketconfiguration', models.Model),
        ),
        migrations.CreateModel(
            name='FemaleYokeConfiguration',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('processing.yokeconfiguration', models.Model),
        ),
    ]
