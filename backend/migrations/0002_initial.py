# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import smart_selects.db_fields
import backend.models
import dictionaries.models


class Migration(migrations.Migration):

    dependencies = [
        ('dictionaries', '0001_initial'),
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shirt',
            name='back',
            field=models.ForeignKey(related_name='back_shirts', verbose_name='\u0421\u043f\u0438\u043d\u043a\u0430', to='dictionaries.BackType'),
        ),
        migrations.AddField(
            model_name='shirt',
            name='collection',
            field=models.ForeignKey(related_name='shirts', verbose_name='\u041a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u044f', to='backend.Collection', null=True),
        ),
        migrations.AddField(
            model_name='shirt',
            name='custom_buttons',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'type', chained_field=b'custom_buttons_type', verbose_name='\u041a\u0430\u0441\u0442\u043e\u043c\u043d\u044b\u0435 \u043f\u0443\u0433\u043e\u0432\u0438\u0446\u044b', blank=True, to='backend.CustomButtons', null=True),
        ),
        migrations.AddField(
            model_name='shirt',
            name='custom_buttons_type',
            field=models.ForeignKey(related_name='back_shirts', verbose_name='\u0422\u0438\u043f \u043a\u0430\u0441\u0442\u043e\u043c\u043d\u044b\u0445 \u043f\u0443\u0433\u043e\u0432\u0438\u0446', blank=True, to='dictionaries.CustomButtonsType', null=True),
        ),
        migrations.AddField(
            model_name='shirt',
            name='fabric',
            field=models.ForeignKey(verbose_name='\u0422\u043a\u0430\u043d\u044c', to='backend.Fabric', null=True),
        ),
        migrations.AddField(
            model_name='shirt',
            name='fit',
            field=models.ForeignKey(verbose_name='\u0422\u0430\u043b\u0438\u044f', blank=True, to='dictionaries.Fit', null=True),
        ),
        migrations.AddField(
            model_name='shirt',
            name='hem',
            field=models.ForeignKey(related_name='hem_shirts', verbose_name='\u041d\u0438\u0437', to='dictionaries.HemType'),
        ),
        migrations.AddField(
            model_name='shirt',
            name='placket',
            field=models.ForeignKey(related_name='placket_shirts', verbose_name='\u041f\u043e\u043b\u043e\u0447\u043a\u0430', to='dictionaries.PlacketType'),
        ),
        migrations.AddField(
            model_name='shirt',
            name='pocket',
            field=models.ForeignKey(related_name='pocket_shirts', verbose_name='\u041a\u0430\u0440\u043c\u0430\u043d', to='dictionaries.PocketType'),
        ),
        migrations.AddField(
            model_name='shirt',
            name='shawl',
            field=models.ForeignKey(default=dictionaries.models.ResolveDefault(backend.models.ShawlOptions), verbose_name='\u041f\u043b\u0430\u0442\u043e\u043a', to='backend.ShawlOptions', null=True),
        ),
        migrations.AddField(
            model_name='shirt',
            name='size',
            field=models.ForeignKey(verbose_name='\u0420\u0430\u0437\u043c\u0435\u0440', blank=True, to='dictionaries.Size', null=True),
        ),
        migrations.AddField(
            model_name='shirt',
            name='size_option',
            field=models.ForeignKey(verbose_name='\u0412\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0439 \u0432\u0430\u0440\u0438\u0430\u043d\u0442 \u0440\u0430\u0437\u043c\u0435\u0440\u0430', to='dictionaries.SizeOptions'),
        ),
        migrations.AddField(
            model_name='shirt',
            name='sleeve',
            field=models.ForeignKey(related_name='sleeve_shirts', default=dictionaries.models.ResolveDefault(dictionaries.models.SleeveType), verbose_name='\u0420\u0443\u043a\u0430\u0432', to='dictionaries.SleeveType'),
        ),
        migrations.AddField(
            model_name='shirt',
            name='sleeve_length',
            field=models.ForeignKey(verbose_name='\u0414\u043b\u0438\u043d\u0430 \u0440\u0443\u043a\u0430\u0432\u0430', blank=True, to='dictionaries.SleeveLength', null=True),
        ),
        migrations.AddField(
            model_name='shirt',
            name='yoke',
            field=models.ForeignKey(verbose_name='\u041a\u043e\u043a\u0435\u0442\u043a\u0430', to='dictionaries.YokeType', null=True),
        ),
        migrations.AddField(
            model_name='initials',
            name='color',
            field=models.ForeignKey(verbose_name='\u0426\u0432\u0435\u0442', to='dictionaries.Color'),
        ),
        migrations.AddField(
            model_name='initials',
            name='font',
            field=models.ForeignKey(verbose_name='\u0428\u0440\u0438\u0444\u0442', to='dictionaries.Font', null=True),
        ),
        migrations.AddField(
            model_name='initials',
            name='shirt',
            field=models.OneToOneField(related_name='initials', to='backend.Shirt'),
        ),
        migrations.AddField(
            model_name='hardness',
            name='collections',
            field=models.ManyToManyField(related_name='hardness', verbose_name='\u041a\u043e\u043b\u043b\u0435\u043a\u0446\u0438\u0438', to='backend.Collection'),
        ),
        migrations.AddField(
            model_name='fabricresidual',
            name='fabric',
            field=models.ForeignKey(related_name='residuals', verbose_name='\u0422\u043a\u0430\u043d\u044c', to='backend.Fabric'),
        ),
        migrations.AddField(
            model_name='fabricresidual',
            name='storehouse',
            field=models.ForeignKey(related_name='residuals', verbose_name='\u0421\u043a\u043b\u0430\u0434', to='backend.Storehouse'),
        ),
        migrations.AddField(
            model_name='fabricprice',
            name='fabric_category',
            field=models.ForeignKey(related_name='prices', verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f \u0442\u043a\u0430\u043d\u0435\u0439', to='dictionaries.FabricCategory'),
        ),
        migrations.AddField(
            model_name='fabricprice',
            name='storehouse',
            field=models.ForeignKey(related_name='prices', verbose_name='\u0421\u043a\u043b\u0430\u0434', to='backend.Storehouse'),
        ),
        migrations.AddField(
            model_name='fabric',
            name='category',
            field=models.ForeignKey(related_name='fabrics', verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f', blank=True, to='dictionaries.FabricCategory', null=True),
        ),
        migrations.AddField(
            model_name='fabric',
            name='colors',
            field=models.ManyToManyField(related_name='color_fabrics', verbose_name='\u0426\u0432\u0435\u0442\u0430', to='dictionaries.FabricColor'),
        ),
        migrations.AddField(
            model_name='fabric',
            name='designs',
            field=models.ManyToManyField(related_name='design_fabrics', verbose_name='\u0414\u0438\u0437\u0430\u0439\u043d', to='dictionaries.FabricDesign'),
        ),
    ]
