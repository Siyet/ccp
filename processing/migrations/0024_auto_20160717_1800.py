# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import processing.storage
import processing.upload_path


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('processing', '0023_auto_20160713_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='StitchesSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('projection', models.CharField(max_length=5, verbose_name='\u041f\u0440\u043e\u0435\u043a\u0446\u0438\u044f', choices=[(b'front', '\u041f\u0435\u0440\u0435\u0434\u043d\u044f\u044f'), (b'side', '\u0411\u043e\u043a\u043e\u0432\u0430\u044f'), (b'back', '\u0417\u0430\u0434\u043d\u044f\u044f')])),
                ('type', models.CharField(default=b'under', max_length=10, verbose_name='\u0420\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435', choices=[(b'under', '\u041f\u043e\u0434 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430\u043c\u0438'), (b'over', '\u041d\u0430\u0434 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430\u043c\u0438')])),
                ('image', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'stitches/%s/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0424\u0430\u0439\u043b \u043d\u0438\u0442\u043e\u043a')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': '\u041c\u043e\u0434\u0435\u043b\u044c \u0441\u0431\u043e\u0440\u043a\u0438 \u043d\u0438\u0442\u043e\u043a',
                'verbose_name_plural': '\u041c\u043e\u0434\u0435\u043b\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u043d\u0438\u0442\u043e\u043a',
            },
        ),
        migrations.AlterField(
            model_name='composesource',
            name='ao',
            field=models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/ao/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0422\u0435\u043d\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='composesource',
            name='light',
            field=models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/light/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0421\u0432\u0435\u0442', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='stitchessource',
            unique_together=set([('content_type', 'object_id', 'projection')]),
        ),
    ]
