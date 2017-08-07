
import random
from django.core.management.base import BaseCommand, CommandError
from core.test.factories import CompanyFactory
from invoices.test.factories import InvoiceFactory, InvoiceItemFactory

class Command(BaseCommand):
    help = 'Generate application dummy data'

    num_companies = 50
    num_invoices = 50

    def handle(self, *args, **options):
        for _ in range(self.num_companies):
            company = CompanyFactory()
            for _ in range(self.num_companies):
                invoice = InvoiceFactory.create(company=company)
                for _ in range(random.randint(1, 10)):
                    InvoiceItemFactory.create(invoice=invoice)

        self.stdout.write("{} companies created each with {} invoices" \
                          .format(self.num_companies, self.num_invoices))
