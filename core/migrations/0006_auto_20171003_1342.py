# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 13:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_merge_20170926_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='dds',
            field=models.CharField(max_length=255, null=True),
        ),
    ]