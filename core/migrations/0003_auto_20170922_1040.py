# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 10:40
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170920_1813'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'base_manager_name': '_plain_manager'},
        ),
        migrations.AlterModelManagers(
            name='company',
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('_plain_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
