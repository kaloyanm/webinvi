# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-15 13:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0019_auto_20171013_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='note',
            field=models.TextField(blank=True, default=''),
        ),
    ]
