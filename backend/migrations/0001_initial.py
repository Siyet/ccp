# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import colorful.fields
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessoriesPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_pk', models.IntegerField(null=True, verbose_name='object ID', blank=True)),
                ('price', models.DecimalField(verbose_name='\u0426\u0435\u043d\u0430', max_digits=10, decimal_places=2)),
            ],
            options={
                'verbose_name': '\u0426\u0435\u043d\u0430 \u043d\u0430\u0434\u0431\u0430\u0432\u043a\u0438',
                'verbose_name_plural': '\u0426\u0435\u043d\u044b \u043d\u0430\u0434\u0431\u0430\u0432\u043e\u043a',
            },
        ),
        migrations.CreateModel(
            name='Collar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': '\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a',
                'verbose_name_plural': '\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('filter_title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0434\u043b\u044f \u0444\u0438\u043b\u044c\u0442\u0440\u0430')),
                ('text', models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('image', models.ImageField(upload_to=b'collection', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
                ('dickey', models.BooleanField(verbose_name='\u041c\u0430\u043d\u0438\u0448\u043a\u0430')),
                ('clasp', models.BooleanField(verbose_name='\u0417\u0430\u0441\u0442\u0435\u0436\u043a\u0430 \u043f\u043e\u0434 \u0448\u0442\u0438\u0444\u0442\u044b')),
                ('solid_yoke', models.BooleanField(verbose_name='\u0426\u0435\u043b\u044c\u043d\u0430\u044f \u043a\u043e\u043a\u0435\u0442\u043a\u0430')),
                ('shawl', models.BooleanField(verbose_name='\u041f\u043b\u0430\u0442\u043e\u043a')),
                ('sex', models.CharField(default=b'male', max_length=6, verbose_name='\u041f\u043e\u043b \u043a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u0438', choices=[(b'male', '\u041c\u0443\u0436\u0441\u043a\u0430\u044f'), (b'female', '\u0416\u0435\u043d\u0441\u043a\u0430\u044f'), (b'unisex', '\u0423\u043d\u0438\u0441\u0435\u043a\u0441')])),
                ('tailoring_time', models.CharField(max_length=255, null=True, verbose_name='\u0412\u0440\u0435\u043c\u044f \u043f\u043e\u0448\u0438\u0432\u0430 \u0438 \u0434\u043e\u0441\u0442\u0430\u0432\u043a\u0438')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u041a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u044f',
                'verbose_name_plural': '\u041a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u0438',
            },
        ),
        migrations.CreateModel(
            name='ContrastDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('element', models.CharField(max_length=20, verbose_name='\u042d\u043b\u0435\u043c\u0435\u043d\u0442', choices=[(b'collar_face', '\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a \u043b\u0438\u0446\u0435\u0432\u0430\u044f \u0441\u0442\u043e\u0440\u043e\u043d\u0430'), (b'collar_bottom', '\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a \u043d\u0438\u0437'), (b'collar_outer', '\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a \u0432\u043d\u0435\u0448\u043d\u044f\u044f \u0441\u0442\u043e\u0439\u043a\u0430'), (b'collar_inner', '\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a \u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u044f \u0441\u0442\u043e\u0439\u043a\u0430'), (b'cuff_outer', '\u041c\u0430\u043d\u0436\u0435\u0442\u0430 \u0432\u043d\u0435\u0448\u043d\u044f\u044f'), (b'cuff_inner', '\u041c\u0430\u043d\u0436\u0435\u0442\u0430 \u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u044f')])),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0442\u0440\u0430\u0441\u0442\u043d\u0430\u044f \u0434\u0435\u0442\u0430\u043b\u044c',
                'verbose_name_plural': '\u041a\u043e\u043d\u0442\u0440\u0430\u0441\u0442\u043d\u044b\u0435 \u0434\u0435\u0442\u0430\u043b\u0438',
            },
        ),
        migrations.CreateModel(
            name='ContrastStitch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': '\u041a\u043e\u043d\u0442\u0440\u0430\u0441\u0442\u043d\u0430\u044f \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0430',
                'verbose_name_plural': '\u041a\u043e\u043d\u0442\u0440\u0430\u0441\u0442\u043d\u044b\u0435 \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='Cuff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': '\u041c\u0430\u043d\u0436\u0435\u0442\u0430',
                'verbose_name_plural': '\u041c\u0430\u043d\u0436\u0435\u0442\u044b',
            },
        ),
        migrations.CreateModel(
            name='CustomButtons',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'custombuttons', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
                ('color', colorful.fields.RGBColorField(default=b'#FFFFFF', verbose_name='\u0426\u0432\u0435\u0442')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u041a\u0430\u0441\u0442\u043e\u043c\u043d\u044b\u0435 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u044b',
                'verbose_name_plural': '\u041a\u0430\u0441\u0442\u043e\u043c\u043d\u044b\u0435 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u044b',
            },
        ),
        migrations.CreateModel(
            name='Dickey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': '\u041c\u0430\u043d\u0438\u0448\u043a\u0430',
                'verbose_name_plural': '\u041c\u0430\u043d\u0438\u0448\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='ElementStitch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u041e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0430',
                'verbose_name_plural': '\u041e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='Fabric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('code', models.CharField(unique=True, max_length=20, verbose_name='\u0410\u0440\u0442\u0438\u043a\u0443\u043b')),
                ('short_description', models.TextField(default=b'', verbose_name='\u041a\u0440\u0430\u0442\u043a\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('long_description', models.TextField(default=b'', verbose_name='\u041f\u043e\u043b\u043d\u043e\u0435 \u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('material', models.CharField(default=b'', max_length=255, verbose_name='\u041c\u0430\u0442\u0435\u0440\u0438\u0430\u043b', blank=True)),
                ('dickey', models.BooleanField(default=False, verbose_name='\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u0442\u0441\u044f \u0432 \u043c\u0430\u043d\u0438\u0448\u043a\u0435')),
                ('active', models.BooleanField(default=True, verbose_name='\u0410\u043a\u0442\u0438\u0432\u043d\u0430')),
            ],
            options={
                'ordering': ('code',),
                'abstract': False,
                'verbose_name': '\u0422\u043a\u0430\u043d\u044c',
                'verbose_name_plural': '\u0422\u043a\u0430\u043d\u0438',
            },
        ),
        migrations.CreateModel(
            name='FabricPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('price', models.DecimalField(verbose_name='\u0426\u0435\u043d\u0430', max_digits=10, decimal_places=2)),
            ],
            options={
                'verbose_name': '\u0426\u0435\u043d\u0430 \u0442\u043a\u0430\u043d\u0438',
                'verbose_name_plural': '\u0426\u0435\u043d\u044b \u0442\u043a\u0430\u043d\u0435\u0439',
            },
        ),
        migrations.CreateModel(
            name='FabricResidual',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(default=0, verbose_name='\u041e\u0441\u0442\u0430\u0442\u043e\u043a', max_digits=10, decimal_places=2)),
            ],
            options={
                'verbose_name': '\u041e\u0441\u0442\u0430\u0442\u043e\u043a \u0442\u043a\u0430\u043d\u0438',
                'verbose_name_plural': '\u041e\u0441\u0442\u0430\u0442\u043a\u0438 \u0442\u043a\u0430\u043d\u0435\u0439',
            },
        ),
        migrations.CreateModel(
            name='Hardness',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u0416\u0435\u0441\u0442\u043a\u043e\u0441\u0442\u044c',
                'verbose_name_plural': '\u0416\u0435\u0441\u0442\u043a\u043e\u0441\u0442\u044c',
            },
        ),
        migrations.CreateModel(
            name='Initials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.CharField(max_length=10, verbose_name='\u041c\u0435\u0441\u0442\u043e\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435', choices=[(b'button2', '2 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430'), (b'button3', '3 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430'), (b'button4', '4 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430'), (b'button5', '5 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430'), (b'hem', '\u041d\u0438\u0437 (\u043b)'), (b'pocket', '\u041a\u0430\u0440\u043c\u0430\u043d (\u043b)'), (b'cuff', '\u041c\u0430\u043d\u0436\u0435\u0442\u0430 (\u043b)')])),
                ('text', models.CharField(max_length=255, verbose_name='\u0422\u0435\u043a\u0441\u0442')),
            ],
            options={
                'verbose_name': '\u0418\u043d\u0438\u0446\u0438\u0430\u043b\u044b',
                'verbose_name_plural': '\u0418\u043d\u0438\u0446\u0438\u0430\u043b\u044b',
            },
        ),
        migrations.CreateModel(
            name='ShawlOptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('extra_price', models.DecimalField(verbose_name='\u0414\u043e\u0431\u0430\u0432\u043e\u0447\u043d\u0430\u044f \u0441\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c', max_digits=10, decimal_places=2)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043f\u043b\u0430\u0442\u043a\u0430',
                'verbose_name_plural': '\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043f\u043b\u0430\u0442\u043a\u0430',
            },
        ),
        migrations.CreateModel(
            name='Shirt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_template', models.BooleanField(default=False, verbose_name='\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u0442\u0441\u044f \u043a\u0430\u043a \u0448\u0430\u0431\u043b\u043e\u043d')),
                ('is_standard', models.BooleanField(default=False, verbose_name='\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u0442\u0441\u044f \u043a\u0430\u043a \u0441\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u043d\u044b\u0439 \u0432\u0430\u0440\u0438\u0430\u043d\u0442', editable=False)),
                ('code', models.CharField(max_length=255, null=True, verbose_name='\u0410\u0440\u0442\u0438\u043a\u0443\u043b')),
                ('individualization', models.TextField(null=True, verbose_name='\u0418\u043d\u0434\u0438\u0432\u0438\u0434\u0443\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044f', blank=True)),
                ('showcase_image', models.ImageField(upload_to=b'showcase', null=True, verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0434\u043b\u044f \u0432\u0438\u0442\u0440\u0438\u043d\u044b')),
                ('tuck', models.BooleanField(default=False, verbose_name='\u0412\u044b\u0442\u0430\u0447\u043a\u0438', choices=[(False, '\u0411\u0435\u0437 \u0432\u044b\u0442\u0430\u0447\u043a\u0438'), (True, '\u0421 \u0432\u044b\u0442\u0430\u0447\u043a\u0430\u043c\u0438')])),
                ('clasp', models.BooleanField(default=False, verbose_name='\u0417\u0430\u0441\u0442\u0435\u0436\u043a\u0430 \u043f\u043e\u0434 \u0448\u0442\u0438\u0444\u0442\u044b', choices=[(False, '\u041d\u0435 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u044c \u0437\u0430\u0441\u0442\u0435\u0436\u043a\u0443'), (True, '\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u044c \u0437\u0430\u0441\u0442\u0435\u0436\u043a\u0443')])),
                ('stitch', models.CharField(max_length=10, verbose_name='\u0428\u0438\u0440\u0438\u043d\u0430 \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438', choices=[(b'none', '0 \u043c\u043c (\u0431\u0435\u0437 \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438)'), (b'1mm', '1 \u043c\u043c (\u0442\u043e\u043b\u044c\u043a\u043e \u0441\u044a\u0435\u043c\u043d\u044b\u0435 \u043a\u043e\u0441\u0442\u043e\u0447\u043a\u0438)'), (b'5mm', '5 \u043c\u043c')])),
                ('price', models.DecimalField(verbose_name='\u0426\u0435\u043d\u0430', null=True, editable=False, max_digits=10, decimal_places=2)),
            ],
            options={
                'ordering': ('code',),
                'verbose_name': '\u0420\u0443\u0431\u0430\u0448\u043a\u0430',
                'verbose_name_plural': '\u0420\u0443\u0431\u0430\u0448\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='ShirtImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'showcase', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
                ('shirt', models.ForeignKey(related_name='shirt_images', to='backend.Shirt')),
            ],
            options={
                'verbose_name': '\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435',
                'verbose_name_plural': '\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f',
            },
        ),
        migrations.CreateModel(
            name='Stays',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('collections', models.ManyToManyField(related_name='stays', verbose_name='\u041a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u0438', to='backend.Collection')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u041a\u043e\u0441\u0442\u043e\u0447\u043a\u0438',
                'verbose_name_plural': '\u041a\u043e\u0441\u0442\u043e\u0447\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='Storehouse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', models.CharField(unique=True, max_length=255, verbose_name='\u0421\u0442\u0440\u0430\u043d\u0430')),
            ],
            options={
                'verbose_name': '\u0421\u043a\u043b\u0430\u0434',
                'verbose_name_plural': '\u0421\u043a\u043b\u0430\u0434\u044b',
            },
        ),
    ]
