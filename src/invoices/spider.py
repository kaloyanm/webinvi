# -*- coding: utf-8 -*-

import os
import json
import re

import scrapy
from bs4 import BeautifulSoup
from django.conf import settings


class LoginFakturiSpider(scrapy.Spider):

    name = 'fakturi.com'
    start_urls = ['https://fakturi.com/actions/login.php']
    invoices_list_url = 'https://fakturi.com/panel.php?page={}'
    invoice_url = 'https://fakturi.com/invoice.php?id={}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_counter = 0
        self.data = []

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={"eik": settings.FAKTURI_EIK, "pass": settings.FAKTURI_PASSWORD},
            callback=self.after_login
        )

    def after_login(self, response):
        # always try the first page
        self.page_counter += 1
        page = self.invoices_list_url.format(self.page_counter)
        return scrapy.http.Request(page, callback=self.parse_list)

    def parse_list(self, response):
        html_content = response.body.decode(response.encoding)
        if "Microinvest" in html_content:
            soup = BeautifulSoup(html_content, "lxml")
            spawned = self.fetch(soup)

            if "по-стари фактури" in html_content:
                self.page_counter += 1
                page = self.invoices_list_url.format(self.page_counter)
                r = scrapy.http.Request(page, callback=self.parse_list)
                spawned.append(r)

            return spawned

    def fetch(self, soup):
        tasks = []
        for tr in soup.find_all("tr"):
            if "onclick" in tr.attrs:
                found = re.findall(r'\d+', tr.attrs['onclick'])
                item_id = int(found.pop())

                full_invoice_url = self.invoice_url.format(item_id)
                r = scrapy.http.Request(full_invoice_url, callback=self.save)
                tasks.append(r)
        return tasks

    def save(self, response):
        html_content = response.body.decode(response.encoding)
        soup = BeautifulSoup(html_content, "lxml")

        data = {}
        data['proforma'] = True if "ПРОФОРМА" in html_content else False
        for input in soup.find_all('input'):
            if "name" in input.attrs and "value" in input.attrs:
                data[input.attrs['name']] = input.attrs['value']

        invoice_dump = "{}.json".format(data['number'])
        invoice_path = os.path.join(settings.FAKTURI_EXPORT_PATH, invoice_dump)
        if os.path.exists(invoice_path):
            return

        with open(invoice_path, "w") as fp:
            json.dump(data, fp)
            print("{} saved!".format(invoice_path))
