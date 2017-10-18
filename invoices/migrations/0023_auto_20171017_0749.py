# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 07:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0022_auto_20171017_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='number',
            field=models.PositiveIntegerField(db_index=True, default=0),
            preserve_default=False,
        ),
    ]