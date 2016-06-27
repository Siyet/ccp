# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0011_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u0418\u043c\u044f')),
                ('lastname', models.CharField(max_length=255, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f')),
                ('midname', models.CharField(max_length=255, verbose_name='\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e')),
                ('phone', models.CharField(max_length=255, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d')),
                ('type', models.CharField(default=b'customer_address', max_length=50, verbose_name='\u0422\u0438\u043f \u0430\u0434\u0440\u0435\u0441\u0430', choices=[(b'customer_address', '\u0410\u0434\u0440\u0435\u0441 \u043a\u043b\u0438\u0435\u043d\u0442\u0430'), (b'other_address', '\u0414\u0440\u0443\u0433\u043e\u0439 \u0430\u0434\u0440\u0435\u0441 (\u0438\u043b\u0438 \u0430\u0434\u0440\u0435\u0441 \u0434\u0440\u0443\u0433\u043e\u0433\u043e \u0447\u0435\u043b\u043e\u0432\u0435\u043a\u0430)')])),
                ('city', models.CharField(max_length=255, verbose_name='\u0413\u043e\u0440\u043e\u0434')),
                ('address', models.CharField(max_length=255, verbose_name='\u0410\u0434\u0440\u0435\u0441')),
                ('index', models.CharField(max_length=6, verbose_name='\u0418\u043d\u0434\u0435\u043a\u0441')),
            ],
            options={
                'verbose_name': '\u0414\u0430\u043d\u043d\u044b\u0435 \u043a\u043b\u0438\u0435\u043d\u0442\u0430',
                'verbose_name_plural': '\u0414\u0430\u043d\u043d\u044b\u0435 \u043a\u043b\u0438\u0435\u043d\u0442\u0430',
            },
        ),
        migrations.RemoveField(
            model_name='orderaddress',
            name='order',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='index',
        ),
        migrations.RemoveField(
            model_name='order',
            name='lastname',
        ),
        migrations.RemoveField(
            model_name='order',
            name='midname',
        ),
        migrations.RemoveField(
            model_name='order',
            name='name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='phone',
        ),
        migrations.AlterField(
            model_name='order',
            name='checkout_shop',
            field=models.ForeignKey(related_name='orders', verbose_name='\u041c\u0430\u0433\u0430\u0437\u0438\u043d', to_field=b'index', blank=True, to='checkout.Shop', null=True),
        ),
        migrations.AlterField(
            model_name='shop',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True),
        ),
        migrations.DeleteModel(
            name='OrderAddress',
        ),
        migrations.AddField(
            model_name='customerdata',
            name='order',
            field=models.ForeignKey(related_name='customer_data', verbose_name='\u0417\u0430\u043a\u0430\u0437', to_field=b'number', to='checkout.Order'),
        ),
    ]
