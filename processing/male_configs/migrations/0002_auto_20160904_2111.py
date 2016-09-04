# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0004_delete_fit'),
        ('male_configs', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BodyConfiguration',
            new_name='MaleBodyConfiguration'
        ),
        migrations.RenameModel(
            old_name='PlacketConfiguration',
            new_name='MalePlacketConfiguration',
        ),
        migrations.AlterModelOptions(
            name='malebodybuttonsconfiguration',
            options={'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043e\u0441\u043d\u043e\u0432\u043d\u044b\u0445 \u043f\u0443\u0433\u043e\u0432\u0438\u0446', 'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043e\u0441\u043d\u043e\u0432\u043d\u044b\u0445 \u043f\u0443\u0433\u043e\u0432\u0438\u0446'},
        ),
        migrations.AlterModelOptions(
            name='malecuffbuttonsconfiguration',
            options={'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043f\u0443\u0433\u043e\u0432\u0438\u0446 \u043c\u0430\u043d\u0436\u0435\u0442', 'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043f\u0443\u0433\u043e\u0432\u0438\u0446 \u043c\u0430\u043d\u0436\u0435\u0442'},
        ),
        migrations.AlterModelOptions(
            name='malecuffconfiguration',
            options={'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043c\u0430\u043d\u0436\u0435\u0442', 'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043c\u0430\u043d\u0436\u0435\u0442'},
        ),
        migrations.AlterModelOptions(
            name='maleinitialsconfiguration',
            options={'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0438\u043d\u0438\u0446\u0438\u0430\u043b\u043e\u0432', 'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0438\u043d\u0438\u0446\u0438\u0430\u043b\u043e\u0432'},
        ),
        migrations.AlterModelOptions(
            name='malepocketconfiguration',
            options={'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043a\u0430\u0440\u043c\u0430\u043d\u0430', 'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043a\u0430\u0440\u043c\u0430\u043d\u0430'},
        ),
        migrations.AlterModelOptions(
            name='maleyokeconfiguration',
            options={'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043a\u043e\u043a\u0435\u0442\u043a\u0438', 'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043a\u043e\u043a\u0435\u0442\u043a\u0438'},
        ),
    ]