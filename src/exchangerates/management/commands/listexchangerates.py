# -*- coding: utf-8 -*-

from __future__ import absolute_import
from django.core.management.base import BaseCommand
from exchangerates.rates import OpenExchangeRatesClient

class Command(BaseCommand):

    def handle(self, *args, **options):
        client = OpenExchangeRatesClient()
        print(client.latest)
