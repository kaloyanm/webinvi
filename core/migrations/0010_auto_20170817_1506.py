# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-08-17 15:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20170817_1445'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyaccess',
            name='invitation_date',
        ),
        migrations.AddField(
            model_name='companyaccess',
            name='expire_on',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='companyaccess',
            name='invitation_key',
            field=models.CharField(db_index=True, max_length=155),
        ),
    ]
