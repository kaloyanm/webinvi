
import factory
from invoices.models import Invoice
from core.test.factories import CompanyFactory

class InvoiceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Invoice

    company = CompanyFactory.create()
