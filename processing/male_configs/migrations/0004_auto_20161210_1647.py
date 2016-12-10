# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import processing.storage
import processing.upload_path


def migrate_body_sources(apps, scheme_editor):
    MaleBodySource = apps.get_model('male_configs', 'MaleBodySource')
    ComposeSource = apps.get_model('processing', 'ComposeSource')
    for s in ComposeSource.objects.filter(content_type__model='malebodyconfiguration'):
        mbs = MaleBodySource(content_type=s.content_type,
                             object_id=s.object_id,
                             projection=s.projection,
                             uv=s.uv,
                             ao=s.ao,
                             light=s.light,
                             shadow=s.shadow)
        mbs.save()
        s.delete()


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('male_configs', '0003_auto_20160910_1834'),
        ('processing', '0010_auto_20160912_1727')
    ]

    operations = [
        migrations.CreateModel(
            name='MaleBodySource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('projection',
                 models.CharField(max_length=5, verbose_name='\u041f\u0440\u043e\u0435\u043a\u0446\u0438\u044f',
                                  choices=[(b'front', '\u041f\u0435\u0440\u0435\u0434\u043d\u044f\u044f'),
                                           (b'side', '\u0411\u043e\u043a\u043e\u0432\u0430\u044f'),
                                           (b'back', '\u0417\u0430\u0434\u043d\u044f\u044f')])),
                ('uv', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/uv/%s'),
                                        storage=processing.storage.OverwriteStorage(), verbose_name='UV')),
                ('ao', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/ao/%s'),
                                        storage=processing.storage.OverwriteStorage(), verbose_name='AO', blank=True)),
                ('light', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/light/%s'),
                                           storage=processing.storage.OverwriteStorage(),
                                           verbose_name='\u0421\u0432\u0435\u0442', blank=True)),
                ('shadow', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/shadow/%s'),
                                            storage=processing.storage.OverwriteStorage(),
                                            verbose_name='\u0422\u0435\u043d\u0438', blank=True)),
                ('object_id', models.PositiveIntegerField()),
                (
                'tuck', models.ForeignKey(to='dictionaries.TuckType', null=True, default=None, verbose_name='\u0412\u044b\u0442\u0430\u0447\u043a\u0438')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
                'verbose_name': '\u041c\u043e\u0434\u0435\u043b\u044c \u0441\u0431\u043e\u0440\u043a\u0438',
                'verbose_name_plural': '\u041c\u043e\u0434\u0435\u043b\u0438 \u0441\u0431\u043e\u0440\u043a\u0438',
            },
        ),
        migrations.AlterUniqueTogether(
            name='malebodysource',
            unique_together=set([('content_type', 'object_id', 'projection', 'tuck')]),
        ),
        migrations.RunPython(migrate_body_sources)
    ]
