# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20171003_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='address_tr',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='city_tr',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='mol_tr',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='name_tr',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
