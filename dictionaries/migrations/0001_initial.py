# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import colorful.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u0441\u043f\u0438\u043d\u043a\u0438',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0441\u043f\u0438\u043d\u043e\u043a',
            },
        ),
        migrations.CreateModel(
            name='CollarButtons',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('buttons', models.IntegerField(default=1, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043f\u0443\u0433\u043e\u0432\u0438\u0446', choices=[(0, 0), (1, 1), (2, 2)])),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u041f\u0443\u0433\u043e\u0432\u0438\u0446\u044b \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
                'verbose_name_plural': '\u041f\u0443\u0433\u043e\u0432\u0438\u0446\u044b \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
            },
        ),
        migrations.CreateModel(
            name='CollarType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
                ('buttons', models.ManyToManyField(to='dictionaries.CollarButtons', verbose_name='\u0412\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u043f\u0443\u0433\u043e\u0432\u0438\u0446')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u0422\u0438\u043f \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u0430',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u043e\u0432',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default='', max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('color', colorful.fields.RGBColorField(verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0426\u0432\u0435\u0442 (\u0434\u043b\u044f \u0438\u043d\u0438\u0446\u0438\u0430\u043b\u043e\u0432)',
                'verbose_name_plural': '\u0426\u0432\u0435\u0442\u0430 (\u0434\u043b\u044f \u0438\u043d\u0438\u0446\u0438\u0430\u043b\u043e\u0432)',
            },
        ),
        migrations.CreateModel(
            name='CuffRounding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u044f \u043c\u0430\u043d\u0436\u0435\u0442\u044b',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u044f \u043c\u0430\u043d\u0436\u0435\u0442\u044b',
            },
        ),
        migrations.CreateModel(
            name='CuffType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
                ('rounding', models.ManyToManyField(to='dictionaries.CuffRounding', verbose_name='\u0412\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u044f', blank=True)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u0422\u0438\u043f \u043c\u0430\u043d\u0436\u0435\u0442\u044b',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u043c\u0430\u043d\u0436\u0435\u0442',
            },
        ),
        migrations.CreateModel(
            name='CustomButtonsType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('extra_price', models.DecimalField(verbose_name='\u0414\u043e\u0431\u0430\u0432\u043e\u0447\u043d\u0430\u044f \u0441\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c', max_digits=10, decimal_places=2)),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u043f\u0443\u0433\u043e\u0432\u0438\u0446',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u043f\u0443\u0433\u043e\u0432\u0438\u0446',
            },
        ),
        migrations.CreateModel(
            name='DefaultElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_pk', models.PositiveIntegerField(verbose_name='\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u043e \u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e')),
                ('content_type', models.OneToOneField(verbose_name='\u0422\u0438\u043f \u044d\u043b\u0435\u043c\u0435\u043d\u0442\u0430', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': '\u042d\u043b\u0435\u043c\u0435\u043d\u0442 \u043f\u043e \u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e',
                'verbose_name_plural': '\u042d\u043b\u0435\u043c\u0435\u043d\u0442\u044b \u043f\u043e \u0443\u043c\u043e\u043b\u0447\u0430\u043d\u0438\u044e',
            },
        ),
        migrations.CreateModel(
            name='DickeyType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u043c\u0430\u043d\u0438\u0448\u043a\u0438',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u043c\u0430\u043d\u0438\u0448\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='FabricCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=1, verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f', db_index=True)),
            ],
            options={
                'verbose_name': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f \u0442\u043a\u0430\u043d\u0438',
                'verbose_name_plural': '\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u0438 \u0442\u043a\u0430\u043d\u0435\u0439',
            },
        ),
        migrations.CreateModel(
            name='FabricColor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('value', colorful.fields.RGBColorField(verbose_name='\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u0426\u0432\u0435\u0442 \u0442\u043a\u0430\u043d\u0438',
                'verbose_name_plural': '\u0426\u0432\u0435\u0442\u0430 \u0442\u043a\u0430\u043d\u0435\u0439',
            },
        ),
        migrations.CreateModel(
            name='FabricDesign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u041f\u0430\u0442\u0442\u0435\u0440\u043d \u0442\u043a\u0430\u043d\u0438',
                'verbose_name_plural': '\u041f\u0430\u0442\u0442\u0435\u0440\u043d\u044b \u0442\u043a\u0430\u043d\u0435\u0439',
            },
        ),
        migrations.CreateModel(
            name='FabricType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u0422\u0438\u043f')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u0422\u0438\u043f \u0442\u043a\u0430\u043d\u0438',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0442\u043a\u0430\u043d\u0435\u0439',
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_add', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f')),
                ('question', models.TextField(max_length=1000, verbose_name='\u0412\u043e\u043f\u0440\u043e\u0441')),
                ('answer', models.TextField(max_length=1000, verbose_name='\u041e\u0442\u0432\u0435\u0442')),
            ],
            options={
                'ordering': ('-date_add',),
                'verbose_name': '\u0412\u043e\u043f\u0440\u043e\u0441',
                'verbose_name_plural': '\u0412\u043e\u043f\u0440\u043e\u0441\u044b \u0438 \u043e\u0442\u0432\u0435\u0442\u044b',
            },
        ),
        migrations.CreateModel(
            name='Fit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u0422\u0438\u043f \u0442\u0430\u043b\u0438\u0438',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0442\u0430\u043b\u0438\u0438',
            },
        ),
        migrations.CreateModel(
            name='Font',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('font', models.FileField(upload_to=b'fonts', verbose_name='\u0424\u0430\u0439\u043b \u0448\u0440\u0438\u0444\u0442\u0430')),
            ],
            options={
                'verbose_name': '\u0428\u0440\u0438\u0444\u0442 (\u0434\u043b\u044f \u0438\u043d\u0438\u0446\u0438\u0430\u043b\u043e\u0432)',
                'verbose_name_plural': '\u0428\u0440\u0438\u0444\u0442\u044b (\u0434\u043b\u044f \u0438\u043d\u0438\u0446\u0438\u0430\u043b\u043e\u0432)',
            },
        ),
        migrations.CreateModel(
            name='HemType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u043d\u0438\u0437\u0430',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u043d\u0438\u0437\u0430',
            },
        ),
        migrations.CreateModel(
            name='PlacketType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
                ('show_buttons', models.BooleanField(default=True, verbose_name='\u041f\u0443\u0433\u043e\u0432\u0438\u0446\u044b \u0432\u0438\u0434\u043d\u044b')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u043f\u043e\u043b\u043e\u0447\u043a\u0438',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u043f\u043e\u043b\u043e\u0447\u0435\u043a',
            },
        ),
        migrations.CreateModel(
            name='PocketType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u043a\u0430\u0440\u043c\u0430\u043d\u0430',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u043a\u0430\u0440\u043c\u0430\u043d\u043e\u0432',
            },
        ),
        migrations.CreateModel(
            name='ShirtInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a')),
                ('text', models.TextField(verbose_name='\u0422\u0435\u043a\u0441\u0442 \u043f\u043e\u0434 \u0437\u0430\u0433\u043e\u043b\u043e\u0432\u043a\u043e\u043c')),
            ],
            options={
                'verbose_name': '\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043e \u0440\u0443\u0431\u0430\u0448\u043a\u0430\u0445',
                'verbose_name_plural': '\u0418\u043d\u0444\u043e\u0440\u043c\u0430\u0446\u0438\u044f \u043e \u0440\u0443\u0431\u0430\u0448\u043a\u0430\u0445',
            },
        ),
        migrations.CreateModel(
            name='ShirtInfoImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'shirtinfo', verbose_name='\u0424\u0430\u0439\u043b')),
                ('text', models.TextField(verbose_name='\u0422\u0435\u043a\u0441\u0442 \u043f\u043e\u0434 \u0438\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435\u043c')),
                ('shirt_info', models.ForeignKey(related_name='images', to='dictionaries.ShirtInfo')),
            ],
            options={
                'verbose_name': '\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435',
                'verbose_name_plural': '\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f',
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('size', models.PositiveIntegerField(unique=True, serialize=False, verbose_name='\u0420\u0430\u0437\u043c\u0435\u0440', primary_key=True)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u0420\u0430\u0437\u043c\u0435\u0440 \u0440\u0443\u0431\u0430\u0448\u043a\u0438',
                'verbose_name_plural': '\u0420\u0430\u0437\u043c\u0435\u0440\u044b \u0440\u0443\u0431\u0430\u0448\u0435\u043a',
            },
        ),
        migrations.CreateModel(
            name='SizeOptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('show_sizes', models.BooleanField(default=True, verbose_name='\u041f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0442\u044c \u0440\u0430\u0437\u043c\u0435\u0440\u044b')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u0412\u0430\u0440\u0438\u0430\u043d\u0442 \u0440\u0430\u0437\u043c\u0435\u0440\u0430',
                'verbose_name_plural': '\u0412\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u0440\u0430\u0437\u043c\u0435\u0440\u043e\u0432',
            },
        ),
        migrations.CreateModel(
            name='SleeveLength',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u0422\u0438\u043f \u0434\u043b\u0438\u043d\u044b \u0440\u0443\u043a\u0430\u0432\u0430',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0434\u043b\u0438\u043d\u044b \u0440\u0443\u043a\u0430\u0432\u0430',
            },
        ),
        migrations.CreateModel(
            name='SleeveType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
                ('cuffs', models.BooleanField(default=True, verbose_name='\u041c\u0430\u043d\u0436\u0435\u0442\u044b')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u0440\u0443\u043a\u0430\u0432\u0430',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u0440\u0443\u043a\u0430\u0432\u043e\u0432',
            },
        ),
        migrations.CreateModel(
            name='StitchColor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('color', colorful.fields.RGBColorField(verbose_name='\u0426\u0432\u0435\u0442')),
            ],
            options={
                'verbose_name': '\u0426\u0432\u0435\u0442 \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438',
                'verbose_name_plural': '\u0426\u0432\u0435\u0442\u0430 \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='Thickness',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
                'verbose_name': '\u0422\u043e\u043b\u0449\u0438\u043d\u0430 \u0442\u043a\u0430\u043d\u0438',
                'verbose_name_plural': '\u0422\u043e\u043b\u0449\u0438\u043d\u0430 \u0442\u043a\u0430\u043d\u0438',
            },
        ),
        migrations.CreateModel(
            name='YokeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'component', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
            ],
            options={
                'verbose_name': '\u0422\u0438\u043f \u043a\u043e\u043a\u0435\u0442\u043a\u0438',
                'verbose_name_plural': '\u0422\u0438\u043f\u044b \u043a\u043e\u043a\u0435\u0442\u043a\u0438',
            },
        ),
        migrations.AddField(
            model_name='cuffrounding',
            name='types',
            field=models.ManyToManyField(to='dictionaries.CuffType', verbose_name='\u0422\u0438\u043f\u044b', blank=True),
        ),
        migrations.AddField(
            model_name='collarbuttons',
            name='types',
            field=models.ManyToManyField(to='dictionaries.CollarType', verbose_name='\u0422\u0438\u043f\u044b \u0432\u043e\u0440\u043e\u0442\u043d\u0438\u043a\u043e\u0432', blank=True),
        ),
    ]
