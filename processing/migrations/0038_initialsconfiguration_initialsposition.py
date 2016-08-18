# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0031_plackettype_show_buttons'),
        ('processing', '0037_auto_20160815_1456'),
    ]

    operations = [
        migrations.CreateModel(
            name='InitialsConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('font_size', models.IntegerField(default=18, verbose_name='\u0420\u0430\u0437\u043c\u0435\u0440 \u0448\u0440\u0438\u0444\u0442\u0430')),
                ('location', models.CharField(max_length=10, verbose_name='\u041c\u0435\u0441\u0442\u043e\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435', choices=[(b'button2', '2 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430'), (b'button3', '3 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430'), (b'button4', '4 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430'), (b'button5', '5 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430'), (b'hem', '\u041d\u0438\u0437 (\u043b)'), (b'pocket', '\u041a\u0430\u0440\u043c\u0430\u043d (\u043b)'), (b'cuff', '\u041c\u0430\u043d\u0436\u0435\u0442\u0430 (\u043b)')])),
                ('font', models.ForeignKey(verbose_name='\u0428\u0440\u0438\u0444\u0442', to='dictionaries.Font')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0438\u043d\u0438\u0446\u0438\u0430\u043b\u043e\u0432',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0438\u043d\u0438\u0446\u0438\u0430\u043b\u043e\u0432',
            },
        ),
        migrations.CreateModel(
            name='InitialsPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('projection', models.CharField(max_length=5, verbose_name='\u041f\u0440\u043e\u0435\u043a\u0446\u0438\u044f', choices=[(b'front', '\u041f\u0435\u0440\u0435\u0434\u043d\u044f\u044f'), (b'side', '\u0411\u043e\u043a\u043e\u0432\u0430\u044f'), (b'back', '\u0417\u0430\u0434\u043d\u044f\u044f')])),
                ('left', models.FloatField(verbose_name='\u041a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u0430 X')),
                ('top', models.FloatField(verbose_name='\u041a\u043e\u043e\u0440\u0434\u0438\u043d\u0430\u0442\u0430 Y')),
                ('rotate', models.IntegerField(default=0, verbose_name='\u041f\u043e\u0432\u043e\u0440\u043e\u0442')),
                ('configuration', models.ForeignKey(related_name='positions', to='processing.InitialsConfiguration')),
            ],
            options={
                'verbose_name': '\u041f\u043e\u0437\u0438\u0446\u0438\u044f \u0438\u043d\u0438\u0446\u0438\u0430\u043b\u043e\u0432',
                'verbose_name_plural': '\u041f\u043e\u0437\u0438\u0446\u0438\u0438 \u0438\u043d\u0438\u0446\u0438\u0430\u043b\u043e\u0432',
            },
        ),
    ]
