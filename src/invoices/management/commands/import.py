# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import json

from datetime import datetime, date
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction
from django.core.paginator import Paginator

from invoices.models import Invoice, InvoiceItem
from core.models import Company


class Command(BaseCommand):
    # local field vs. remote field
    mapping = {
        "client_name": "client_name",
        "client_eik": "client_eik",
        "client_dds": "client_dds_no",
        "client_city": "client_city",
        "client_address": "client_address",
        "client_mol": "client_mol",
        "payment_swift": "swift",
        "payment_type": "pay_method",
        "payment_iban": "iban",
        "payment_bank": "bank",
        "note": "notice",
        "no_dds_reason": "dds_cause",
        "created_by": "author",
        "accepted_by": "receiver",
        "number": "number",
        "released_at": "date",
        "taxevent_at": "date_event"
    }

    def add_arguments(self, parser):
        parser.add_argument("--user-id", required=True, type=int)
    
    def str_to_datefield(self, str_date):
        dt = datetime.strptime(str_date, "%d.%m.%Y")
        conv_date = date(year=dt.year, month=dt.month, day=dt.day)
        return conv_date
        
    def handle(self, *args, **options):

        try:
            user = User.objects.get(pk=options["user_id"])
        except User.DoesNotExist:
            raise CommandError("Invalid user {}".format(options["user_id"]))

        try:
            company = Company.objects.get(user=user, default=True)
        except Company.DoesNotExist:
            raise CommandError("Missing default company for user {}".format(options["user_id"]))

        Invoice.objects.filter(company=company).delete()

        imported = 0
        for root, dirs, files in os.walk(settings.FAKTURI_EXPORT_PATH):
            for name in files:
                invoice_path = os.path.join(root, name)

                with open(invoice_path) as fp:
                    invoice = {}
                    invoice_items = []
                    content = json.load(fp)

                    for local, remote in self.mapping.items():
                        if remote in content:
                            invoice[local] = content[remote]

                    if "collection" in content:
                        invoice_items = self.prepare_invoice_items( content.get("collection") )

                    content["number"] = int(content["number"])
                    invoice["invoice_type"] = "proforma" if content.get("proforma") else "invoice"
                    invoice["released_at"] = self.str_to_datefield(invoice["released_at"])
                    invoice["taxevent_at"] = self.str_to_datefield(invoice["taxevent_at"])
                    
                    self.save(invoice, invoice_items, company)
                    imported += 1

        self.stdout.write(self.style.SUCCESS("{} invoices have been imported successfuly".format(imported)))
    
    def prepare_invoice_items(self, collection):
        items = []
        paginator = Paginator(collection, 5)
        
        for p in paginator.page_range:
            page = paginator.page(p)
            
            item = {}
            for prop in page.object_list:
                key, values = list(prop.keys()).pop(), list(prop.values())
                item[key.replace("[]", "")] = values.pop()
            items.append(item)
        return items

    def save(self, invoice, invoice_items, company):
        
        with transaction.atomic():
            instance = Invoice(**invoice)
            instance.company = company
            print(instance.released_at)
            instance.save()
            
            for item in invoice_items:
                entry = InvoiceItem(**item)
                entry.invoice = instance
                entry.save()
    
