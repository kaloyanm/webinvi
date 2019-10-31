import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from core.test.factories import CompanyFactory, UserFactory
from invoices.test.factories import InvoiceFactory, InvoiceItemFactory


class Command(BaseCommand):
    help = 'Generate application dummy data'

    def handle(self, *args, **options):
        User = get_user_model()
        User.objects.all().delete()

        num_of_invoices = 25
        num_of_users = 10
        output_message = "{} users created each with {} invoices"\
            .format(num_of_users, num_of_invoices)

        for _ in range(num_of_users):
            user = UserFactory.create()
            user.set_password("test1234")
            user.save()

            for _ in range(num_of_invoices):
                invoice = InvoiceFactory.create(user=user)
                for _ in range(random.randint(1, 10)):
                    InvoiceItemFactory.create(invoice=invoice)

        self.stdout.write(output_message)
