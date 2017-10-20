# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-20 09:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0023_auto_20171017_0749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_type',
            field=models.CharField(choices=[('invoice', 'Фактура'), ('proforma', 'Проформа'), ('credit', 'Кредит'), ('debit', 'Дебит')], default='invoice', max_length=10),
        ),
    ]