
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
        comp_per_user = 10
        inv_per_company = 50
        num_users = 10
        output_message = "{} users created each with {} companies each with {} invoices"\
            .format(num_users, comp_per_user, inv_per_company)

        User = get_user_model()
        User.objects.all().delete()
        Company.objects.all().delete()

        while num_users > 0:
            user = UserFactory.create()
            user.set_password("test1234")
            user.save()

            counter = comp_per_user
            while counter > 0:
                company = CompanyFactory(user=user)
                company.save()
                counter -= 1

                counter2 = inv_per_company
                while counter2 > 0:
                    invoice = InvoiceFactory.create(company=company)
                    for _ in range(random.randint(1, 10)):
                        InvoiceItemFactory.create(invoice=invoice)
                    counter2 -= 1

            num_users -= 1

        self.stdout.write(output_message)
