# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 12:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0025_invoiceitem_dds_percent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_type',
            field=models.CharField(choices=[('invoice', 'Фактура'), ('proforma', 'Проформа'), ('credit', 'Кредит'), ('debit', 'Дебит')], db_index=True, default='invoice', max_length=10),
        ),
    ]
