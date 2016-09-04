# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0004_delete_fit'),
    ]

    operations = [
        migrations.CreateModel(
            name='DickeyConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dickey', models.ForeignKey(verbose_name='\u0422\u0438\u043f \u043c\u0430\u043d\u0438\u0448\u043a\u0438', to='dictionaries.DickeyType')),
                ('hem', models.ForeignKey(verbose_name='\u041d\u0438\u0437', blank=True, to='dictionaries.HemType', null=True)),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043c\u0430\u043d\u0438\u0448\u043a\u0438',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043c\u0430\u043d\u0438\u0448\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='MaleBackConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('back', models.ForeignKey(verbose_name='\u0421\u043f\u0438\u043d\u043a\u0430', to='dictionaries.BackType')),
                ('hem', models.ForeignKey(verbose_name='\u041d\u0438\u0437', to='dictionaries.HemType')),
                ('tuck', models.ForeignKey(verbose_name='\u0412\u044b\u0442\u0430\u0447\u043a\u0438', to='dictionaries.TuckType')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u0441\u043f\u0438\u043d\u043a\u0438',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u0441\u043f\u0438\u043d\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='BodyConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cuff_types', models.ManyToManyField(to='dictionaries.CuffType', verbose_name='\u0422\u0438\u043f\u044b \u043c\u0430\u043d\u0436\u0435\u0442')),
                ('hem', models.ForeignKey(verbose_name='\u041d\u0438\u0437', to='dictionaries.HemType')),
                ('sleeve', models.ForeignKey(verbose_name='\u0420\u0443\u043a\u0430\u0432', to='dictionaries.SleeveType')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043e\u0441\u043d\u043e\u0432\u044b',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043e\u0441\u043d\u043e\u0432\u044b',
            },
        ),
        migrations.CreateModel(
            name='MaleCollarButtonsConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buttons', models.IntegerField(default=1, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u0443\u0433\u043e\u0432\u0438\u0446', choices=[(0, 0), (1, 1), (2, 2)])),
                ('collar', models.ForeignKey(verbose_name='\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a', to='dictionaries.CollarType')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043f\u0443\u0433\u043e\u0432\u0438\u0446 \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043f\u0443\u0433\u043e\u0432\u0438\u0446 \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
            },
        ),
        migrations.CreateModel(
            name='MaleCollarConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buttons', models.IntegerField(default=1, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u0443\u0433\u043e\u0432\u0438\u0446', choices=[(0, 0), (1, 1), (2, 2)])),
                ('collar', models.ForeignKey(verbose_name='\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a', to='dictionaries.CollarType')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
            },
        ),
        migrations.CreateModel(
            name='PlacketConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hem', models.ForeignKey(verbose_name='\u041d\u0438\u0437', to='dictionaries.HemType')),
                ('plackets', models.ManyToManyField(to='dictionaries.PlacketType', verbose_name='\u0422\u0438\u043f \u043f\u043e\u043b\u043e\u0447\u043a\u0438')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043f\u043e\u043b\u043e\u0447\u043a\u0438',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043f\u043e\u043b\u043e\u0447\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='MaleBodyButtonsConfiguration',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('processing.bodybuttonsconfiguration', models.Model),
        ),
        migrations.CreateModel(
            name='MaleCuffButtonsConfiguration',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('processing.cuffbuttonsconfiguration', models.Model),
        ),
        migrations.CreateModel(
            name='MaleCuffConfiguration',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('processing.cuffconfiguration', models.Model),
        ),
        migrations.CreateModel(
            name='MaleInitialsConfiguration',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('processing.initialsconfiguration', models.Model),
        ),
        migrations.CreateModel(
            name='MalePocketConfiguration',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('processing.pocketconfiguration', models.Model),
        ),
        migrations.CreateModel(
            name='MaleYokeConfiguration',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('processing.yokeconfiguration', models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='malecollarconfiguration',
            unique_together=set([('collar', 'buttons')]),
        ),
        migrations.AlterUniqueTogether(
            name='malecollarbuttonsconfiguration',
            unique_together=set([('collar', 'buttons')]),
        ),
        migrations.AlterUniqueTogether(
            name='malebackconfiguration',
            unique_together=set([('back', 'hem', 'tuck')]),
        ),
        migrations.AlterUniqueTogether(
            name='dickeyconfiguration',
            unique_together=set([('dickey', 'hem')]),
        ),
    ]
