# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-06 13:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='released_at',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='tax_event_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
