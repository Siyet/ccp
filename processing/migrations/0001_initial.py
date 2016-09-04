# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import processing.storage
import django.utils.timezone
import model_utils.fields
import processing.upload_path
import processing.models.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_initial'),
        ('dictionaries', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tuck', models.BooleanField(default=False, verbose_name='\u0412\u044b\u0442\u0430\u0447\u043a\u0438', choices=[(False, '\u0411\u0435\u0437 \u0432\u044b\u0442\u0430\u0447\u043a\u0438'), (True, '\u0421 \u0432\u044b\u0442\u0430\u0447\u043a\u0430\u043c\u0438')])),
                ('back', models.ForeignKey(verbose_name='\u0421\u043f\u0438\u043d\u043a\u0430', to='dictionaries.BackType')),
                ('hem', models.ForeignKey(verbose_name='\u041d\u0438\u0437', to='dictionaries.HemType')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u0441\u043f\u0438\u043d\u043a\u0438',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u0441\u043f\u0438\u043d\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='BodyButtonsConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('buttons', models.OneToOneField(verbose_name='\u041f\u0443\u0433\u043e\u0432\u0438\u0446\u044b', to='dictionaries.CustomButtonsType')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043e\u0441\u043d\u043e\u0432\u043d\u044b\u0445 \u043f\u0443\u0433\u043e\u0432\u0438\u0446',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043e\u0441\u043d\u043e\u0432\u043d\u044b\u0445 \u043f\u0443\u0433\u043e\u0432\u0438\u0446',
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
            name='ButtonsSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('projection', models.CharField(max_length=5, verbose_name='\u041f\u0440\u043e\u0435\u043a\u0446\u0438\u044f', choices=[(b'front', '\u041f\u0435\u0440\u0435\u0434\u043d\u044f\u044f'), (b'side', '\u0411\u043e\u043a\u043e\u0432\u0430\u044f'), (b'back', '\u0417\u0430\u0434\u043d\u044f\u044f')])),
                ('image', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/buttons/image/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
                ('ao', models.FileField(storage=processing.storage.OverwriteStorage(), upload_to=processing.upload_path.UploadComposingSource(b'%s/buttons/ao/%s'), null=True, verbose_name='\u0422\u0435\u043d\u0438', blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': '\u041c\u043e\u0434\u0435\u043b\u044c \u0441\u0431\u043e\u0440\u043a\u0438 \u043f\u0443\u0433\u043e\u0432\u0438\u0446',
                'verbose_name_plural': '\u041c\u043e\u0434\u0435\u043b\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u043f\u0443\u0433\u043e\u0432\u0438\u0446',
            },
        ),
        migrations.CreateModel(
            name='CollarButtonsConfiguration',
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
            name='CollarConfiguration',
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
            name='CollarMask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('projection', models.CharField(max_length=5, verbose_name='\u041f\u0440\u043e\u0435\u043a\u0446\u0438\u044f', choices=[(b'front', '\u041f\u0435\u0440\u0435\u0434\u043d\u044f\u044f'), (b'side', '\u0411\u043e\u043a\u043e\u0432\u0430\u044f'), (b'back', '\u0417\u0430\u0434\u043d\u044f\u044f')])),
                ('mask', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'composesource/%s/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0424\u0430\u0439\u043b \u043c\u0430\u0441\u043a\u0438')),
                ('element', models.CharField(max_length=20, verbose_name='\u042d\u043b\u0435\u043c\u0435\u043d\u0442', choices=[(b'collar_face', '\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a \u043b\u0438\u0446\u0435\u0432\u0430\u044f \u0441\u0442\u043e\u0440\u043e\u043d\u0430'), (b'collar_bottom', '\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a \u043d\u0438\u0437'), (b'collar_outer', '\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a \u0432\u043d\u0435\u0448\u043d\u044f\u044f \u0441\u0442\u043e\u0439\u043a\u0430'), (b'collar_inner', '\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a \u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u044f \u0441\u0442\u043e\u0439\u043a\u0430')])),
                ('collar', models.ForeignKey(related_name='masks', to='processing.CollarConfiguration')),
            ],
            options={
                'verbose_name': '\u041c\u0430\u0441\u043a\u0430 \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
                'verbose_name_plural': '\u041c\u0430\u0441\u043a\u0438 \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
            },
        ),
        migrations.CreateModel(
            name='ComposeSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('projection', models.CharField(max_length=5, verbose_name='\u041f\u0440\u043e\u0435\u043a\u0446\u0438\u044f', choices=[(b'front', '\u041f\u0435\u0440\u0435\u0434\u043d\u044f\u044f'), (b'side', '\u0411\u043e\u043a\u043e\u0432\u0430\u044f'), (b'back', '\u0417\u0430\u0434\u043d\u044f\u044f')])),
                ('uv', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/uv/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='UV')),
                ('ao', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/ao/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0422\u0435\u043d\u0438', blank=True)),
                ('light', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'%s/light/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0421\u0432\u0435\u0442', blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': '\u041c\u043e\u0434\u0435\u043b\u044c \u0441\u0431\u043e\u0440\u043a\u0438',
                'verbose_name_plural': '\u041c\u043e\u0434\u0435\u043b\u0438 \u0441\u0431\u043e\u0440\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='CuffButtonsConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cuff', models.ForeignKey(verbose_name='\u0422\u0438\u043f \u043c\u0430\u0436\u0435\u0442\u044b', to='dictionaries.CuffType')),
                ('rounding_types', models.ManyToManyField(to='dictionaries.CuffRounding', verbose_name='\u0422\u0438\u043f\u044b \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u044f', blank=True)),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043f\u0443\u0433\u043e\u0432\u0438\u0446 \u043c\u0430\u043d\u0436\u0435\u0442',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043f\u0443\u0433\u043e\u0432\u0438\u0446 \u043c\u0430\u043d\u0436\u0435\u0442',
            },
        ),
        migrations.CreateModel(
            name='CuffConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('side_mask', models.FileField(storage=processing.storage.OverwriteStorage(), upload_to=processing.upload_path.UploadComposingSource(b'composesource/%s/%s'), null=True, verbose_name='\u041c\u0430\u0441\u043a\u0430 \u0440\u0443\u043a\u0430\u0432\u0430 (\u0441\u0431\u043e\u043a\u0443)')),
                ('cuff_types', models.ManyToManyField(to='dictionaries.CuffType', verbose_name='\u0422\u0438\u043f\u044b \u043c\u0430\u043d\u0436\u0435\u0442')),
                ('rounding', models.ForeignKey(verbose_name='\u0422\u0438\u043f \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u044f', blank=True, to='dictionaries.CuffRounding', null=True)),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043c\u0430\u043d\u0436\u0435\u0442',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043c\u0430\u043d\u0436\u0435\u0442',
            },
        ),
        migrations.CreateModel(
            name='CuffMask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('projection', models.CharField(max_length=5, verbose_name='\u041f\u0440\u043e\u0435\u043a\u0446\u0438\u044f', choices=[(b'front', '\u041f\u0435\u0440\u0435\u0434\u043d\u044f\u044f'), (b'side', '\u0411\u043e\u043a\u043e\u0432\u0430\u044f'), (b'back', '\u0417\u0430\u0434\u043d\u044f\u044f')])),
                ('mask', models.FileField(upload_to=processing.upload_path.UploadComposingSource(b'composesource/%s/%s'), storage=processing.storage.OverwriteStorage(), verbose_name='\u0424\u0430\u0439\u043b \u043c\u0430\u0441\u043a\u0438')),
                ('element', models.CharField(max_length=20, verbose_name='\u042d\u043b\u0435\u043c\u0435\u043d\u0442', choices=[(b'cuff_outer', '\u041c\u0430\u043d\u0436\u0435\u0442\u0430 \u0432\u043d\u0435\u0448\u043d\u044f\u044f'), (b'cuff_inner', '\u041c\u0430\u043d\u0436\u0435\u0442\u0430 \u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u044f')])),
                ('cuff', models.ForeignKey(related_name='masks', to='processing.CuffConfiguration')),
            ],
            options={
                'verbose_name': '\u041c\u0430\u0441\u043a\u0430 \u043c\u0430\u043d\u0436\u0435\u0442\u044b',
                'verbose_name_plural': '\u041c\u0430\u0441\u043a\u0438 \u043c\u0430\u043d\u0436\u0435\u0442',
            },
        ),
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
            name='InitialsConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('font_size', models.IntegerField(default=18, verbose_name='\u0420\u0430\u0437\u043c\u0435\u0440 \u0448\u0440\u0438\u0444\u0442\u0430')),
                ('location', models.CharField(max_length=10, verbose_name='\u041c\u0435\u0441\u0442\u043e\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435', choices=[(b'button2', '2 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430'), (b'button3', '3 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430'), (b'button4', '4 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430'), (b'button5', '5 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430'), (b'hem', '\u041d\u0438\u0437 (\u043b)'), (b'pocket', '\u041a\u0430\u0440\u043c\u0430\u043d (\u043b)'), (b'cuff', '\u041c\u0430\u043d\u0436\u0435\u0442\u0430 (\u043b)')])),
                ('font', models.ForeignKey(verbose_name='\u0428\u0440\u0438\u0444\u0442', to='dictionaries.Font')),
                ('pocket', models.ManyToManyField(to='dictionaries.PocketType', verbose_name='\u0412\u0438\u0434\u043d\u043e \u0441 \u043a\u0430\u0440\u043c\u0430\u043d\u043e\u043c')),
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
            name='PocketConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pocket', models.OneToOneField(verbose_name='\u0422\u0438\u043f \u043a\u0430\u0440\u043c\u0430\u043d\u0430', to='dictionaries.PocketType')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043a\u0430\u0440\u043c\u0430\u043d\u0430',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043a\u0430\u0440\u043c\u0430\u043d\u0430',
            },
        ),
        migrations.CreateModel(
            name='SourceCache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resolution', models.CharField(default=b'preview', max_length=10, choices=[(b'full', b'full'), (b'preview', b'preview')])),
                ('source_field', models.CharField(max_length=10)),
                ('pos_repr', models.CommaSeparatedIntegerField(max_length=20)),
                ('file', models.FileField(storage=processing.storage.OverwriteStorage(), upload_to=processing.upload_path.UploadComposeCache(b'composecache/%s/%s/%s'))),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='StitchColor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_type', models.OneToOneField(verbose_name='\u0422\u0438\u043f \u043a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438', to='contenttypes.ContentType')),
                ('element', models.ForeignKey(verbose_name='\u041e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0430', to='backend.ElementStitch')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u0435\u043a',
            },
        ),
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
        migrations.CreateModel(
            name='Texture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('texture', models.ImageField(upload_to=b'textures', storage=processing.storage.OverwriteStorage(), verbose_name='\u0424\u0430\u0439\u043b \u0442\u0435\u043a\u0441\u0442\u0443\u0440\u044b')),
                ('needs_shadow', models.BooleanField(default=True, verbose_name='\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u044c \u0442\u0435\u043d\u0438')),
                ('moire_filter', models.IntegerField(default=0, verbose_name='\u041c\u0443\u0430\u0440 \u0444\u0438\u043b\u044c\u0442\u0440', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0412\u043a\u043b\u044e\u0447\u0435\u043d')])),
            ],
            options={
                'ordering': ('texture',),
                'verbose_name': '\u0422\u0435\u043a\u0441\u0442\u0443\u0440\u0430',
                'verbose_name_plural': '\u0422\u0435\u043a\u0441\u0442\u0443\u0440\u044b',
            },
            bases=(processing.models.mixins.ModelDiffMixin, models.Model),
        ),
        migrations.CreateModel(
            name='YokeConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('yoke', models.OneToOneField(verbose_name='\u0422\u0438\u043f \u043a\u043e\u043a\u0435\u0442\u043a\u0438', to='dictionaries.YokeType')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u044f \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043a\u043e\u043a\u0435\u0442\u043a\u0438',
                'verbose_name_plural': '\u041a\u043e\u043d\u0444\u0438\u0433\u0443\u0440\u0430\u0446\u0438\u0438 \u0441\u0431\u043e\u0440\u043a\u0438 \u0434\u043b\u044f \u043a\u043e\u043a\u0435\u0442\u043a\u0438',
            },
        ),
        migrations.AlterUniqueTogether(
            name='stitchessource',
            unique_together=set([('content_type', 'object_id', 'projection', 'type')]),
        ),
        migrations.AlterUniqueTogether(
            name='sourcecache',
            unique_together=set([('content_type', 'object_id', 'source_field', 'resolution')]),
        ),
        migrations.AlterUniqueTogether(
            name='dickeyconfiguration',
            unique_together=set([('dickey', 'hem')]),
        ),
        migrations.AlterUniqueTogether(
            name='cuffmask',
            unique_together=set([('cuff', 'element', 'projection')]),
        ),
        migrations.AlterUniqueTogether(
            name='composesource',
            unique_together=set([('content_type', 'object_id', 'projection')]),
        ),
        migrations.AlterUniqueTogether(
            name='collarmask',
            unique_together=set([('collar', 'element', 'projection')]),
        ),
        migrations.AlterUniqueTogether(
            name='collarconfiguration',
            unique_together=set([('collar', 'buttons')]),
        ),
        migrations.AlterUniqueTogether(
            name='collarbuttonsconfiguration',
            unique_together=set([('collar', 'buttons')]),
        ),
        migrations.AlterUniqueTogether(
            name='buttonssource',
            unique_together=set([('content_type', 'object_id', 'projection')]),
        ),
        migrations.AlterUniqueTogether(
            name='backconfiguration',
            unique_together=set([('back', 'hem', 'tuck')]),
        ),
    ]