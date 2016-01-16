# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0003_auto_20160115_1816'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stays', models.CharField(max_length=10, verbose_name='\u041a\u043e\u0441\u0442\u043e\u0447\u043a\u0438', choices=[(b'yes', '\u0414\u0430'), (b'no', '\u041d\u0435\u0442'), (b'removable', '\u0414\u0430, \u0441\u044a\u0435\u043c\u043d\u044b\u0435')])),
                ('hardness', models.CharField(max_length=15, verbose_name='\u0416\u0435\u0441\u0442\u043a\u043e\u0441\u0442\u044c', choices=[(b'very_soft', '\u041e\u0447\u0435\u043d\u044c \u043c\u044f\u0433\u043a\u0438\u0439'), (b'soft', '\u041c\u044f\u0433\u043a\u0438\u0439'), (b'hard', '\u0416\u0435\u0441\u0442\u043a\u0438\u0439'), (b'very_hard', '\u041e\u0447\u0435\u043d\u044c \u0436\u0435\u0441\u0442\u043a\u0438\u0439'), (b'no_hardener', '\u0411\u0435\u0437 \u0443\u043f\u043b\u043e\u0442\u043d\u0438\u0442\u0435\u043b\u044f')])),
                ('type', models.ForeignKey(verbose_name='\u0422\u0438\u043f', to='dictionaries.CollarType')),
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
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('dickey', models.BooleanField(verbose_name='\u041c\u0430\u043d\u0438\u0448\u043a\u0430')),
                ('clasp', models.BooleanField(verbose_name='\u0417\u0430\u0441\u0442\u0435\u0436\u043a\u0430 \u043f\u043e\u0434 \u0448\u0442\u0438\u0444\u0442\u044b')),
                ('solid_yoke', models.BooleanField(verbose_name='\u0426\u0435\u043b\u044c\u043d\u0430\u044f \u043a\u043e\u043a\u0435\u0442\u043a\u0430')),
                ('shawl', models.BooleanField(verbose_name='\u041f\u043b\u0430\u0442\u043e\u043a')),
            ],
            options={
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
                ('element', models.CharField(max_length=10, verbose_name='\u042d\u043b\u0435\u043c\u0435\u043d\u0442', choices=[(b'shirt', '\u0421\u043e\u0440\u043e\u0447\u043a\u0430'), (b'cuffs', '\u041c\u0430\u043d\u0436\u0435\u0442\u044b'), (b'collar', '\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a'), (b'thread', '\u041f\u0435\u0442\u0435\u043b\u044c/\u043d\u0438\u0442\u043e\u043a')])),
                ('color', models.ForeignKey(verbose_name='\u0426\u0432\u0435\u0442 \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438', to='dictionaries.StitchColor')),
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
                ('hardness', models.CharField(max_length=15, verbose_name='\u0416\u0435\u0441\u0442\u043a\u043e\u0441\u0442\u044c', choices=[(b'very_soft', '\u041e\u0447\u0435\u043d\u044c \u043c\u044f\u0433\u043a\u0438\u0439'), (b'soft', '\u041c\u044f\u0433\u043a\u0438\u0439'), (b'hard', '\u0416\u0435\u0441\u0442\u043a\u0438\u0439'), (b'very_hard', '\u041e\u0447\u0435\u043d\u044c \u0436\u0435\u0441\u0442\u043a\u0438\u0439'), (b'no_hardener', '\u0411\u0435\u0437 \u0443\u043f\u043b\u043e\u0442\u043d\u0438\u0442\u0435\u043b\u044f')])),
                ('sleeve', models.BooleanField(verbose_name='\u0420\u0443\u043a\u0430\u0432')),
                ('type', models.ForeignKey(verbose_name='\u0422\u0438\u043f', to='dictionaries.CuffType')),
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
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('picture', models.ImageField(upload_to=b'', verbose_name='\u0418\u0437\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435')),
                ('type', models.ForeignKey(verbose_name='\u0422\u0438\u043f', to='dictionaries.CustomButtonsType')),
            ],
            options={
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
            name='Fabric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=20, verbose_name='\u0410\u0440\u0442\u0438\u043a\u0443\u043b')),
                ('description', models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435')),
                ('texture', models.ImageField(upload_to=b'', verbose_name='\u0422\u0435\u043a\u0441\u0442\u0443\u0440\u0430')),
                ('colors', models.ManyToManyField(related_name='color_fabrics', verbose_name='\u0426\u0432\u0435\u0442\u0430', to='dictionaries.FabricColor')),
                ('designs', models.ManyToManyField(related_name='design_fabrics', verbose_name='\u0414\u0438\u0437\u0430\u0439\u043d', to='dictionaries.FabricColor')),
            ],
            options={
                'verbose_name': '\u0422\u043a\u0430\u043d\u044c',
                'verbose_name_plural': '\u0422\u043a\u0430\u043d\u0438',
            },
        ),
        migrations.CreateModel(
            name='FabricPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(verbose_name='\u0426\u0435\u043d\u0430', max_digits=10, decimal_places=2)),
                ('fabric', models.ForeignKey(related_name='prices', verbose_name='\u0422\u043a\u0430\u043d\u044c', to='backend.Fabric')),
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
                ('amount', models.DecimalField(verbose_name='\u041e\u0441\u0442\u0430\u0442\u043e\u043a', max_digits=10, decimal_places=2)),
                ('fabric', models.ForeignKey(related_name='residuals', verbose_name='\u0422\u043a\u0430\u043d\u044c', to='backend.Fabric')),
            ],
            options={
                'verbose_name': '\u041e\u0441\u0442\u0430\u0442\u043e\u043a \u0442\u043a\u0430\u043d\u0438',
                'verbose_name_plural': '\u041e\u0441\u0442\u0430\u0442\u043a\u0438 \u0442\u043a\u0430\u043d\u0435\u0439',
            },
        ),
        migrations.CreateModel(
            name='Initials',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('font', models.CharField(max_length=10, verbose_name='\u0428\u0440\u0438\u0444\u0442', choices=[(b'script', b'Script'), (b'arial', b'Arial'), (b'free', b'Free')])),
                ('location', models.CharField(max_length=10, verbose_name='\u041c\u0435\u0441\u0442\u043e\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435', choices=[(b'button2', '2 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430'), (b'button3', '3 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430'), (b'button4', '4 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430'), (b'button5', '5 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u0430'), (b'hem', '\u041d\u0438\u0437 (\u043b)'), (b'pocket', '\u041a\u0430\u0440\u043c\u0430\u043d (\u043b)'), (b'cuff', '\u041c\u0430\u043d\u0436\u0435\u0442\u0430 (\u043b)')])),
                ('text', models.CharField(max_length=255, verbose_name='\u0422\u0435\u043a\u0441\u0442')),
                ('color', models.ForeignKey(verbose_name='\u0426\u0432\u0435\u0442', to='dictionaries.Color')),
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
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('extra_price', models.DecimalField(verbose_name='\u0414\u043e\u0431\u0430\u0432\u043e\u0447\u043d\u0430\u044f \u0441\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c', max_digits=10, decimal_places=2)),
            ],
            options={
                'verbose_name': '\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043f\u043b\u0430\u0442\u043a\u0430',
                'verbose_name_plural': '\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043f\u043b\u0430\u0442\u043a\u0430',
            },
        ),
        migrations.CreateModel(
            name='Shirt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_template', models.BooleanField(verbose_name='\u0418\u0441\u043f\u043e\u043b\u044c\u0437\u0443\u0435\u0442\u0441\u044f \u043a\u0430\u043a \u0448\u0430\u0431\u043b\u043e\u043d')),
                ('size', models.IntegerField(verbose_name='\u0420\u0430\u0437\u043c\u0435\u0440', choices=[(35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42)])),
                ('hem', models.CharField(max_length=10, verbose_name='\u041d\u0438\u0437', choices=[(b'straight', '\u041f\u0440\u044f\u043c\u043e\u0439'), (b'figured', '\u0424\u0438\u0433\u0443\u0440\u043d\u044b\u0439')])),
                ('placket', models.CharField(max_length=10, verbose_name='\u041f\u043e\u043b\u043e\u0447\u043a\u0430', choices=[(b'plank', '\u0421 \u043f\u043b\u0430\u043d\u043a\u043e\u0439'), (b'hidden', '\u0421\u043a\u0440\u044b\u0442\u0430\u044f \u0437\u0430\u0441\u0442\u0435\u0436\u043a\u0430'), (b'no_plank', '\u0411\u0435\u0437 \u043f\u043b\u0430\u043d\u043a\u0438')])),
                ('pocket', models.CharField(max_length=10, verbose_name='\u041a\u0430\u0440\u043c\u0430\u043d', choices=[(b'none', '\u0411\u0435\u0437 \u043a\u0430\u0440\u043c\u0430\u043d\u0430'), (b'rounded', '\u0417\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u043d\u044b\u0435 \u0443\u0433\u043b\u044b'), (b'straight', '\u041f\u0440\u044f\u043c\u044b\u0435 \u0443\u0433\u043b\u044b')])),
                ('tuck', models.BooleanField(verbose_name='\u0412\u044b\u0442\u0430\u0447\u043a\u0438')),
                ('back', models.CharField(max_length=10, verbose_name='\u0421\u043f\u0438\u043d\u043a\u0430', choices=[(b'no_folds', '\u0411\u0435\u0437 \u0441\u043a\u043b\u0430\u0434\u043e\u043a'), (b'one_fold', '\u041e\u0434\u043d\u0430 \u0441\u043a\u043b\u0430\u0434\u043a\u0430'), (b'two_folds', '\u0414\u0432\u0435 \u0441\u043a\u043b\u0430\u0434\u043a\u0438')])),
                ('clasp', models.BooleanField(verbose_name='\u0417\u0430\u0441\u0442\u0435\u0436\u043a\u0430 \u043f\u043e\u0434 \u0448\u0442\u0438\u0444\u0442\u044b')),
                ('stitch', models.CharField(max_length=10, verbose_name='\u0428\u0438\u0440\u0438\u043d\u0430 \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438', choices=[(b'none', '0 \u043c\u043c (\u0431\u0435\u0437 \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438)'), (b'1mm', '1 \u043c\u043c (\u0442\u043e\u043b\u044c\u043a\u043e \u0441\u044a\u0435\u043c\u043d\u044b\u0435 \u043a\u043e\u0441\u0442\u043e\u0447\u043a\u0438)'), (b'5mm', '5 \u043c\u043c')])),
                ('collar', models.OneToOneField(verbose_name='\u0412\u043e\u0440\u043e\u0442\u043d\u0438\u043a', to='backend.Collar')),
                ('cuffs', models.OneToOneField(verbose_name='\u041c\u0430\u043d\u0436\u0435\u0442\u044b', to='backend.Cuff')),
                ('custom_buttons', models.ForeignKey(verbose_name='\u041a\u0430\u0441\u0442\u043e\u043c\u043d\u044b\u0435 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u044b', blank=True, to='backend.CustomButtons', null=True)),
                ('dickey', models.OneToOneField(null=True, blank=True, to='backend.Dickey', verbose_name='\u041c\u0430\u043d\u0438\u0448\u043a\u0430')),
                ('fabric', models.ForeignKey(verbose_name='\u0422\u043a\u0430\u043d\u044c', to='backend.Fabric')),
                ('initials', models.OneToOneField(null=True, blank=True, to='backend.Initials', verbose_name='\u0418\u043d\u0438\u0446\u0438\u0430\u043b\u044b')),
                ('shawl', models.ForeignKey(verbose_name='\u041f\u043b\u0430\u0442\u043e\u043a', to='backend.ShawlOptions')),
                ('yoke', models.ForeignKey(verbose_name='\u041a\u043e\u043a\u0435\u0442\u043a\u0430', to='dictionaries.YokeType')),
            ],
            options={
                'verbose_name': '\u0420\u0443\u0431\u0430\u0448\u043a\u0430',
                'verbose_name_plural': '\u0420\u0443\u0431\u0430\u0448\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='Storehouse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('collection', models.ForeignKey(verbose_name='\u041a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u044f', to='backend.Collection')),
            ],
            options={
                'verbose_name': '\u0421\u043a\u043b\u0430\u0434',
                'verbose_name_plural': '\u0421\u043a\u043b\u0430\u0434\u044b',
            },
        ),
        migrations.AddField(
            model_name='fabricresidual',
            name='storehouse',
            field=models.ForeignKey(related_name='residuals', verbose_name='\u0421\u043a\u043b\u0430\u0434', to='backend.Storehouse'),
        ),
        migrations.AddField(
            model_name='fabricprice',
            name='storehouse',
            field=models.ForeignKey(related_name='prices', verbose_name='\u0421\u043a\u043b\u0430\u0434', to='backend.Storehouse'),
        ),
        migrations.AddField(
            model_name='dickey',
            name='fabric',
            field=models.ForeignKey(to='backend.Fabric'),
        ),
        migrations.AddField(
            model_name='dickey',
            name='type',
            field=models.ForeignKey(to='dictionaries.DickeyType'),
        ),
        migrations.AddField(
            model_name='contraststitch',
            name='shirt',
            field=models.ForeignKey(to='backend.Shirt'),
        ),
        migrations.AddField(
            model_name='contrastdetails',
            name='fabric',
            field=models.ForeignKey(verbose_name='\u0422\u043a\u0430\u043d\u044c', to='backend.Fabric'),
        ),
        migrations.AddField(
            model_name='contrastdetails',
            name='shirt',
            field=models.ForeignKey(verbose_name='\u0420\u0443\u0431\u0430\u0448\u043a\u0430', to='backend.Shirt'),
        ),
    ]
