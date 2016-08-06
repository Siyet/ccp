# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('dictionaries', '0027_sleevetype_cuffs'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_pk', models.PositiveIntegerField(verbose_name='\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u043e \u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e')),
                ('content_type', models.OneToOneField(verbose_name='\u0422\u0438\u043f \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0430', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': '\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u043e \u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e',
                'verbose_name_plural': '\u042d\u043b\u0435\u043c\u0435\u043d\u0442\u044b \u043f\u043e \u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e'
            },
        ),
        migrations.AlterUniqueTogether(
            name='defaultelement',
            unique_together=set([('content_type', 'object_pk')]),
        ),
    ]
