# -*- coding: utf-8 -*-

import json

import requests
from django.conf import settings


class OpenExchangeRatesException(Exception):
    pass


class OpenExchangeRatesClient():

    base_api_url = 'https://openexchangerates.org/api/'

    def __init__(self, app_id=None):
        self.app_id = getattr(settings, "OERATES_APP_ID", app_id)


    def _request(self, operation):
        url = "{}{}".format(self.base_api_url, operation)
        payload = {"app_id": self.app_id}

        r = requests.get(url, params=payload)
        result = r.json() or {}

        if "error" in result:
            raise OpenExchangeRatesException(result["description"])
        return result

    @property
    def latest(self):
        return self._request('latest.json')

    @property
    def currencies(self):
        return self._request('currencies.json')

    @property
    def usage(self):
        return self._request('usage.json')
