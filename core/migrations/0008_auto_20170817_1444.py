# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-08-17 14:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20170817_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyaccess',
            name='invitation_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
