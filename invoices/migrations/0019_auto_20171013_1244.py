# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-13 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0018_auto_20171013_1136'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='currency',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='currency_rate',
            field=models.DecimalField(decimal_places=6, max_digits=10, null=True),
        ),
    ]