# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-06 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0004_invoice_invoice_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='invoice_no',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='proforma_no',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
