# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import json

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from invoices.models import Invoice
from core.models import Company

# def import_map_invoice_type(data, field):
#     return "proforma" if data['proforma'] else "invoice"
#
#
# def import_invoice_no(data, field):
#     return data[field] if not data['proforma'] else 0
#
#
# def import_map_proforma_no(data, field):
#     return data[field] if data['proforma'] else 0




class Command(BaseCommand):

    mapping = {
        # "invoice_type": import_map_invoice_type,
        "client_name": "client_name",
        "client_eik": "client_eik",
        "client_dds": "client_dds_no",
        "client_city": "client_city",
        "client_address": "client_address",
        "client_mol": "client_mol",
        # "invoice_no": import_invoice_no,
        # "proforma_no": import_map_proforma_no,
        "payment_swift": "swift",
        "payment_type": "pay_method",
        "payment_iban": "iban",
        "payment_bank": "bank",
        "": "",
        "note": "notice",
        "no_dds_reason": "dds_cause",
        "created_by": "author",
        "accepted_by": "receiver",
    }

    def add_arguments(self, parser):
        parser.add_argument("--user-id", required=True, type=int)

    def handle(self, *args, **options):

        try:
            user = User.objects.get(pk=options["user_id"])
        except User.DoesNotExist:
            raise CommandError("Invalid user {}".format(options["user_id"]))

        try:
            company = Company.objects.get(user=user, default=True)
        except Company.DoesNotExist:
            raise CommandError("Missing default company for user {}".format(options["user_id"]))

        imported = 0
        for root, dirs, files in os.walk(settings.FAKTURI_EXPORT_PATH):
            for name in files:
                invoice_path = os.path.join(root, name)

                with open(invoice_path) as fp:
                    record = {}
                    content = json.load(fp)

                    for local, remote in self.mapping.items():
                        if remote in content:
                            record[local] = content[remote]
                    self.save(record, company)
                    imported += 1

        self.stdout.write(self.style.SUCCESS("{} invoices have been imported successfuly".format(imported)))

    def save(self, record, company):
        invoice = Invoice(**record)
        invoice.company = company
        invoice.save()
        # print(record)
