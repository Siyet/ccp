# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_initial'),
        ('processing', '0001_initial'),
        ('dictionaries', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='fabric',
            name='texture',
            field=models.OneToOneField(related_name='fabric', null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0422\u0435\u043a\u0441\u0442\u0443\u0440\u0430', to='processing.Texture'),
        ),
        migrations.AddField(
            model_name='fabric',
            name='thickness',
            field=models.ForeignKey(related_name='fabrics', verbose_name='\u0422\u043e\u043b\u0449\u0438\u043d\u0430', to='dictionaries.Thickness', null=True),
        ),
        migrations.AddField(
            model_name='fabric',
            name='type',
            field=models.ForeignKey(related_name='fabrics', verbose_name='\u0422\u0438\u043f', to='dictionaries.FabricType', null=True),
        ),
        migrations.AddField(
            model_name='elementstitch',
            name='collections',
            field=models.ManyToManyField(related_name='stitches', verbose_name='\u041a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u0438', to='backend.Collection'),
        ),
        migrations.AddField(
            model_name='dickey',
            name='fabric',
            field=models.ForeignKey(related_name='dickey_list', verbose_name='\u0422\u043a\u0430\u043d\u044c', to='backend.Fabric'),
        ),
        migrations.AddField(
            model_name='dickey',
            name='shirt',
            field=models.OneToOneField(related_name='dickey', to='backend.Shirt'),
        ),
        migrations.AddField(
            model_name='dickey',
            name='type',
            field=models.ForeignKey(verbose_name='\u0422\u0438\u043f', to='dictionaries.DickeyType'),
        ),
        migrations.AddField(
            model_name='custombuttons',
            name='type',
            field=models.ForeignKey(related_name='buttons', verbose_name='\u0422\u0438\u043f', to='dictionaries.CustomButtonsType'),
        ),
        migrations.AddField(
            model_name='cuff',
            name='hardness',
            field=models.ForeignKey(verbose_name='\u0416\u0435\u0441\u0442\u043a\u043e\u0441\u0442\u044c', to='backend.Hardness', null=True),
        ),
        migrations.AddField(
            model_name='cuff',
            name='rounding',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'types', chained_field=b'type', verbose_name='\u0422\u0438\u043f \u0437\u0430\u043a\u0440\u0443\u0433\u043b\u0435\u043d\u0438\u044f', blank=True, to='dictionaries.CuffRounding', null=True),
        ),
        migrations.AddField(
            model_name='cuff',
            name='shirt',
            field=models.OneToOneField(related_name='cuff', to='backend.Shirt'),
        ),
        migrations.AddField(
            model_name='cuff',
            name='type',
            field=models.ForeignKey(related_name='type_cuffs', verbose_name='\u0422\u0438\u043f', to='dictionaries.CuffType'),
        ),
        migrations.AddField(
            model_name='contraststitch',
            name='color',
            field=models.ForeignKey(verbose_name='\u0426\u0432\u0435\u0442 \u043e\u0442\u0441\u0442\u0440\u043e\u0447\u043a\u0438', to='dictionaries.StitchColor'),
        ),
        migrations.AddField(
            model_name='contraststitch',
            name='element',
            field=models.ForeignKey(verbose_name='\u042d\u043b\u0435\u043c\u0435\u043d\u0442', to='backend.ElementStitch', null=True),
        ),
        migrations.AddField(
            model_name='contraststitch',
            name='shirt',
            field=models.ForeignKey(related_name='contrast_stitches', to='backend.Shirt'),
        ),
        migrations.AddField(
            model_name='contrastdetails',
            name='fabric',
            field=models.ForeignKey(verbose_name='\u0422\u043a\u0430\u043d\u044c', to='backend.Fabric'),
        ),
        migrations.AddField(
            model_name='contrastdetails',
            name='shirt',
            field=models.ForeignKey(related_name='contrast_details', verbose_name='\u0420\u0443\u0431\u0430\u0448\u043a\u0430', to='backend.Shirt'),
        ),
        migrations.AddField(
            model_name='collection',
            name='storehouse',
            field=models.ForeignKey(related_name='collections', verbose_name='\u0421\u043a\u043b\u0430\u0434', to='backend.Storehouse', null=True),
        ),
        migrations.AddField(
            model_name='collar',
            name='hardness',
            field=models.ForeignKey(verbose_name='\u0416\u0435\u0441\u0442\u043a\u043e\u0441\u0442\u044c', to='backend.Hardness', null=True),
        ),
        migrations.AddField(
            model_name='collar',
            name='shirt',
            field=models.OneToOneField(related_name='collar', to='backend.Shirt'),
        ),
        migrations.AddField(
            model_name='collar',
            name='size',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'types', chained_field=b'type', verbose_name='\u041f\u0443\u0433\u043e\u0432\u0438\u0446\u044b', to='dictionaries.CollarButtons', null=True),
        ),
        migrations.AddField(
            model_name='collar',
            name='stays',
            field=models.ForeignKey(verbose_name='\u041a\u043e\u0441\u0442\u043e\u0447\u043a\u0438', to='backend.Stays', null=True),
        ),
        migrations.AddField(
            model_name='collar',
            name='type',
            field=models.ForeignKey(verbose_name='\u0422\u0438\u043f', to='dictionaries.CollarType'),
        ),
        migrations.AddField(
            model_name='accessoriesprice',
            name='collections',
            field=models.ManyToManyField(related_name='accessories_prices', verbose_name='\u041a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u0438', to='backend.Collection', blank=True),
        ),
        migrations.AddField(
            model_name='accessoriesprice',
            name='content_type',
            field=models.ForeignKey(related_name='accessories_price', verbose_name='content type', to='contenttypes.ContentType'),
        ),
        migrations.CreateModel(
            name='CustomShirt',
            fields=[
            ],
            options={
                'verbose_name': '\u0420\u0443\u0431\u0430\u0448\u043a\u0430',
                'proxy': True,
                'verbose_name_plural': '\u0420\u0443\u0431\u0430\u0448\u043a\u0438',
            },
            bases=('backend.shirt',),
        ),
        migrations.CreateModel(
            name='StandardShirt',
            fields=[
            ],
            options={
                'verbose_name': '\u0421\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u043d\u044b\u0439 \u0432\u0430\u0440\u0438\u0430\u043d\u0442 \u0440\u0443\u0431\u0430\u0448\u043a\u0438',
                'proxy': True,
                'verbose_name_plural': '\u0421\u0442\u0430\u043d\u0434\u0430\u0440\u0442\u043d\u044b\u0435 \u0432\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u0440\u0443\u0431\u0430\u0448\u0435\u043a',
            },
            bases=('backend.shirt',),
        ),
        migrations.CreateModel(
            name='TemplateShirt',
            fields=[
            ],
            options={
                'verbose_name': '\u0428\u0430\u0431\u043b\u043e\u043d \u0440\u0443\u0431\u0430\u0448\u043a\u0438',
                'proxy': True,
                'verbose_name_plural': '\u0428\u0430\u0431\u043b\u043e\u043d\u044b \u0440\u0443\u0431\u0430\u0448\u0435\u043a',
            },
            bases=('backend.shirt',),
        ),
        migrations.AlterUniqueTogether(
            name='fabricresidual',
            unique_together=set([('fabric', 'storehouse')]),
        ),
        migrations.AlterUniqueTogether(
            name='contrastdetails',
            unique_together=set([('shirt', 'element')]),
        ),
        migrations.AlterUniqueTogether(
            name='accessoriesprice',
            unique_together=set([('content_type', 'object_pk')]),
        ),
    ]
