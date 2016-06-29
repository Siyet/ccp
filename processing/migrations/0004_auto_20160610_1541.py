# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-10 12:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import processing.models
import processing.upload_path


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0019_auto_20160519_1940'),
        ('processing', '0003_auto_20160607_0957'),
    ]

    operations = [
        migrations.CreateModel(
            name='BodyButtonsSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buttons', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dictionaries.CustomButtonsType', verbose_name='\u041f\u0443\u0433\u043e\u0432\u0438\u0446\u044b')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043e\u0441\u043d\u043e\u0432\u043d\u044b\u0445 \u043f\u0443\u0433\u043e\u0432\u0438\u0446',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043e\u0441\u043d\u043e\u0432\u043d\u044b\u0445 \u043f\u0443\u0433\u043e\u0432\u0438\u0446',
            },
            bases=(models.Model, processing.models.SourceMixin),
        ),
        migrations.CreateModel(
            name='ButtonsSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projection', models.CharField(choices=[(b'front', '\u041f\u0435\u0440\u0435\u0434\u043d\u044f\u044f'), (b'side', '\u0411\u043e\u043a\u043e\u0432\u0430\u044f'), (b'back', '\u0417\u0430\u0434\u043d\u044f\u044f')], max_length=5, verbose_name='\u041f\u0440\u043e\u0435\u043a\u0446\u0438\u044f')),
                ('image', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/buttons/image/%s'), verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
                ('ao', models.FileField(blank=True, null=True, upload_to=processing.upload_path.UploadComposingSource(b'%s/buttons/ao/%s'), verbose_name='\u0422\u0435\u043d\u0438')),
            ],
            options={
                'verbose_name': '\u041c\u043e\u0434\u0435\u043b\u044c \u0441\u0431\u043e\u0440\u043a\u0438 \u043f\u0443\u0433\u043e\u0432\u0438\u0446',
                'verbose_name_plural': '\u041c\u043e\u0434\u0435\u043b\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u043f\u0443\u0433\u043e\u0432\u0438\u0446',
            },
        ),
        migrations.CreateModel(
            name='CollarButtonsSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buttons', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dictionaries.CollarButtons', verbose_name='\u041f\u0443\u0433\u043e\u0432\u0438\u0446\u044b')),
                ('collar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionaries.CollarType', verbose_name='\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043f\u0443\u0433\u043e\u0432\u0438\u0446 \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043f\u0443\u0433\u043e\u0432\u0438\u0446 \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
            },
            bases=(models.Model, processing.models.SourceMixin),
        ),
        migrations.CreateModel(
            name='CuffButtonsSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionaries.CuffType', verbose_name='\u041c\u0430\u043d\u0436\u0435\u0442\u044b')),
                ('rounding', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dictionaries.CuffRounding', verbose_name='\u0422\u0438\u043f \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u044f')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043f\u0443\u0433\u043e\u0432\u0438\u0446 \u043c\u0430\u043d\u0436\u0435\u0442',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043f\u0443\u0433\u043e\u0432\u0438\u0446 \u043c\u0430\u043d\u0436\u0435\u0442',
            },
            bases=(models.Model, processing.models.SourceMixin),
        ),
        migrations.AddField(
            model_name='placketsource',
            name='hem',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='dictionaries.HemType', verbose_name='\u041d\u0438\u0437'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='placketsource',
            unique_together=set([('placket', 'hem')]),
        ),
        migrations.AlterUniqueTogether(
            name='cuffbuttonssource',
            unique_together=set([('cuff', 'rounding')]),
        ),
        migrations.AlterUniqueTogether(
            name='collarbuttonssource',
            unique_together=set([('collar', 'buttons')]),
        ),
    ]