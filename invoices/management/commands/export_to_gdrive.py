# -*- coding: utf-8 -*-

from invoices.tasks import save_invoice_to_google_drive
from django.core.management.base import BaseCommand

import os
import json

from core.models import CredentialsModel


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_id = CredentialsModel.objects.all()[0].id.id
        settings = {
            'gdrive_sync': True,
            'invoice_id': 120,
            'filename': 'test.pdf',
        }
        r = save_invoice_to_google_drive.delay(user_id, settings)
        print(r.get())
