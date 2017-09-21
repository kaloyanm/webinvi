# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-09-20 18:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0005_auto_20170906_1453'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='client_address_bg',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='client_address_en',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='client_address_es',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='client_city_bg',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='client_city_en',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='client_city_es',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='client_mol_bg',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='client_mol_en',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='client_mol_es',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='client_name_bg',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='client_name_en',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='client_name_es',
        ),
        migrations.RemoveField(
            model_name='invoiceitem',
            name='measure_bg',
        ),
        migrations.RemoveField(
            model_name='invoiceitem',
            name='measure_en',
        ),
        migrations.RemoveField(
            model_name='invoiceitem',
            name='measure_es',
        ),
        migrations.RemoveField(
            model_name='invoiceitem',
            name='name_bg',
        ),
        migrations.RemoveField(
            model_name='invoiceitem',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='invoiceitem',
            name='name_es',
        ),
    ]