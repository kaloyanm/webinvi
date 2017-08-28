
import random

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.test.factories import CompanyFactory, UserFactory
from core.models import Company
from invoices.test.factories import InvoiceFactory, InvoiceItemFactory


class Command(BaseCommand):
    help = 'Generate application dummy data'

    num_companies = 10
    num_invoices = 50

    def handle(self, *args, **options):
        User = get_user_model()
        User.objects.all().delete()
        Company.objects.all().delete()

        for _ in range(self.num_companies):
            company = CompanyFactory()
            company.user.set_password("test1234")
            company.user.save()
            for _ in range(self.num_companies):
                invoice = InvoiceFactory.create(company=company)
                for _ in range(random.randint(1, 10)):
                    InvoiceItemFactory.create(invoice=invoice)

        self.stdout.write("{} companies created each with {} invoices" \
                          .format(self.num_companies, self.num_invoices))
