# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import json

from django.core.management.base import BaseCommand
from django.conf import settings
from invoices.models import Invoice


def import_map_invoice_type(data, field):
    return "proforma" if data['proforma'] else "invoice"


def import_invoice_no(data, field):
    return data[field] if not data['proforma'] else 0


def import_map_proforma_no(data, field):
    return data[field] if data['proforma'] else 0


models_json_mapping = {
    "invoice_type": import_map_invoice_type,
    "receiver_name": "client_name",
    "receiver_eik": "client_eik",
    "receiver_dds": "client_dds_no",
    "receiver_city": "client_city",
    "receiver_address": "client_address",
    "receiver_mol": "client_mol",
    "invoice_no": import_invoice_no,
    "proforma_no": import_map_proforma_no,
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

class Command(BaseCommand):

    def handle(self, *args, **options):

        for root, dirs, files in os.walk(settings.FAKTURI_EXPORT_PATH):
            for name in files:
                invoice_path = os.path.join(root, name)
                with open(invoice_path) as fp:
                    content = json.load(fp)
                    print(content)
                    break

