# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-07 10:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20171005_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='dds',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]