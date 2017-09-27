
import random

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.test.factories import CompanyFactory, UserFactory
from core.models import Company
from invoices.test.factories import InvoiceFactory, InvoiceItemFactory


class Command(BaseCommand):
    help = 'Generate application dummy data'

    def handle(self, *args, **options):
        num_companies = 10
        num_invoices = 50
        output_message = "{} companies created each with {} invoices".format(num_companies, num_invoices)

        User = get_user_model()
        User.objects.all().delete()
        Company.objects.all().delete()

        while num_companies > 0:
            company = CompanyFactory(default=True)
            company.user.set_password("test1234")
            company.user.save()

            counter = num_invoices
            while counter > 0:
                invoice = InvoiceFactory.create(company=company)
                for _ in range(random.randint(1, 10)):
                    InvoiceItemFactory.create(invoice=invoice)
                counter -= 1

            num_companies -= 1

        self.stdout.write(output_message)
