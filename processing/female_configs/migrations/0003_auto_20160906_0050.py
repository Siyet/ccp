# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import processing.storage
import processing.upload_path


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('dictionaries', '0004_delete_fit'),
        ('female_configs', '0002_auto_20160904_2008'),
    ]

    operations = [
        migrations.CreateModel(
            name='FemaleBackShadow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shadow', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'composesource/%s/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0424\u0430\u0439\u043b \u0442\u0435\u043d\u0438')),
                ('back', models.OneToOneField(verbose_name='\u0421\u043f\u0438\u043d\u043a\u0430', to='dictionaries.BackType')),
            ],
            options={
                'verbose_name': '\u0422\u0435\u043d\u044c \u0441\u043f\u0438\u043d\u043a\u0438',
                'verbose_name_plural': '\u0422\u0435\u043d\u0438 \u0441\u043f\u0438\u043d\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='FemaleBodySource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('projection', models.CharField(max_length=5, verbose_name='\u041f\u0440\u043e\u0435\u043a\u0446\u0438\u044f', choices=[(b'front', '\u041f\u0435\u0440\u0435\u0434\u043d\u044f\u044f'), (b'side', '\u0411\u043e\u043a\u043e\u0432\u0430\u044f'), (b'back', '\u0417\u0430\u0434\u043d\u044f\u044f')])),
                ('uv', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/uv/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='UV')),
                ('ao', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/ao/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0422\u0435\u043d\u0438', blank=True)),
                ('light', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/light/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0421\u0432\u0435\u0442', blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('back', models.ForeignKey(verbose_name='\u0421\u043f\u0438\u043d\u043a\u0430', blank=True, to='dictionaries.BackType', null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
                'verbose_name': '\u041c\u043e\u0434\u0435\u043b\u044c \u0441\u0431\u043e\u0440\u043a\u0438',
                'verbose_name_plural': '\u041c\u043e\u0434\u0435\u043b\u0438 \u0441\u0431\u043e\u0440\u043a\u0438',
            },
        ),
        migrations.AlterUniqueTogether(
            name='femalebodysource',
            unique_together=set([('content_type', 'object_id', 'projection', 'back')]),
        ),
    ]
