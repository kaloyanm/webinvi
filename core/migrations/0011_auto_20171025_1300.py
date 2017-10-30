# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 13:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_company_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='payment_bank',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='payment_bank_tr',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='payment_iban',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='payment_swift',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='payment_type',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='company',
            name='payment_type_tr',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
