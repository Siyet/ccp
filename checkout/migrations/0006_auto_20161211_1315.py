# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_auto_20161210_1647'),
        ('checkout', '0005_auto_20161211_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u0418\u043c\u044f')),
                ('lastname', models.CharField(max_length=255, verbose_name='\u0424\u0430\u043c\u0438\u043b\u0438\u044f')),
                ('midname', models.CharField(max_length=255, verbose_name='\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e', blank=True)),
                ('phone', models.CharField(max_length=255, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d')),
                ('email', models.EmailField(max_length=255, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d')),
                ('type', models.CharField(default=b'customer_address', max_length=50, verbose_name='\u0422\u0438\u043f \u0430\u0434\u0440\u0435\u0441\u0430', choices=[(b'customer_address', '\u0410\u0434\u0440\u0435\u0441 \u043a\u043b\u0438\u0435\u043d\u0442\u0430'), (b'other_address', '\u0414\u0440\u0443\u0433\u043e\u0439 \u0430\u0434\u0440\u0435\u0441 (\u0438\u043b\u0438 \u0430\u0434\u0440\u0435\u0441 \u0434\u0440\u0443\u0433\u043e\u0433\u043e \u0447\u0435\u043b\u043e\u0432\u0435\u043a\u0430)')])),
                ('city', models.CharField(max_length=255, verbose_name='\u0413\u043e\u0440\u043e\u0434')),
                ('address', models.CharField(max_length=255, verbose_name='\u0410\u0434\u0440\u0435\u0441')),
                ('index', models.CharField(max_length=6, verbose_name='\u0418\u043d\u0434\u0435\u043a\u0441', blank=True)),
            ],
            options={
                'verbose_name': '\u0414\u0430\u043d\u043d\u044b\u0435 \u043a\u043b\u0438\u0435\u043d\u0442\u0430',
                'verbose_name_plural': '\u0414\u0430\u043d\u043d\u044b\u0435 \u043a\u043b\u0438\u0435\u043d\u0442\u0430',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('number', models.AutoField(serialize=False, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0437\u0430\u043a\u0430\u0437\u0430', primary_key=True)),
                ('state', models.CharField(default=b'new', max_length=20, verbose_name='\u0421\u0442\u0430\u0442\u0443\u0441', choices=[(b'new', '\u041e\u0436\u0438\u0434\u0430\u0435\u0442 \u043e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0438'), (b'completed', '\u041e\u0431\u0440\u0430\u0431\u043e\u0442\u0430\u043d')])),
                ('date_add', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430 \u0434\u043e\u0431\u0430\u0432\u043b\u0435\u043d\u0438\u044f', null=True)),
                ('discount_value', models.FloatField(default=0, null=True, verbose_name='\u041d\u043e\u043c\u0438\u043d\u0430\u043b \u0441\u043a\u0438\u0434\u043a\u0438')),
                ('certificate_value', models.PositiveIntegerField(default=0, null=True, verbose_name='\u041d\u043e\u043c\u0438\u043d\u0430\u043b \u0441\u0435\u0440\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u0430')),
                ('certificate', models.ForeignKey(blank=True, to='checkout.Certificate', null=True)),
                ('checkout_shop', models.ForeignKey(related_name='orders', verbose_name='\u041c\u0430\u0433\u0430\u0437\u0438\u043d', to_field=b'index', blank=True, to='checkout.Shop', null=True)),
                ('customer', models.ForeignKey(verbose_name='\u041a\u043b\u0438\u0435\u043d\u0442', to_field=b'number', blank=True, to='checkout.Customer', null=True)),
                ('payment', models.OneToOneField(related_name='order', null=True, blank=True, to='checkout.Payment')),
            ],
            options={
                'verbose_name': '\u0417\u0430\u043a\u0430\u0437',
                'verbose_name_plural': '\u0417\u0430\u043a\u0430\u0437\u044b',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField(verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e')),
                ('price', models.DecimalField(verbose_name='\u0426\u0435\u043d\u0430', null=True, editable=False, max_digits=10, decimal_places=2)),
                ('order', models.ForeignKey(related_name='items', verbose_name='\u0417\u0430\u043a\u0430\u0437', to='checkout.Order')),
                ('shirt', models.ForeignKey(verbose_name='\u0420\u0443\u0431\u0430\u0448\u043a\u0430', to='backend.Shirt')),
            ],
            options={
                'db_table': 'checkout_orderdetails',
                'verbose_name': '\u0414\u0435\u0442\u0430\u043b\u0438 \u0437\u0430\u043a\u0430\u0437\u0430',
                'verbose_name_plural': '\u0414\u0435\u0442\u0430\u043b\u0438 \u0437\u0430\u043a\u0430\u0437\u0430',
            },
        ),
        migrations.AddField(
            model_name='customerdata',
            name='order',
            field=models.ForeignKey(related_name='customer_data', verbose_name='\u0417\u0430\u043a\u0430\u0437', to='checkout.Order'),
        ),
        migrations.AlterUniqueTogether(
            name='customerdata',
            unique_together=set([('order', 'type')]),
        ),
    ]