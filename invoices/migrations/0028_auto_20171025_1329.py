# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0027_auto_20171025_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='payment_type',
            field=models.CharField(choices=[(1, 'Банков превод'), (2, 'В брой'), (3, 'С наложен платеж')], default=1, max_length=255),
        ),
    ]