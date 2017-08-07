import random
import factory
import datetime
from invoices.models import Invoice, InvoiceItem

class InvoiceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Invoice

    company = factory.SubFactory("core.test.factories.CompanyFactory")
    client_name = factory.Faker('company', locale='bg_BG')
    client_eik = factory.Sequence(lambda n: 2345678912 - n) # any ten digits number would suffice
    client_city = factory.Faker('city')
    client_address = factory.Faker('address')
    client_mol = factory.Faker('name')

    invoice_type = random.choice(['invoice', 'proforma'])
    released_at = factory.Faker('date_time_between_dates',
        datetime_start = datetime.datetime(2014, 1, 1),
        datetime_end = datetime.datetime(2017, 1, 1, 20)
    )


class InvoiceItemFactory(factory.DjangoModelFactory):
    class Meta:
        model = InvoiceItem

    invoice = factory.SubFactory('invoices.test.factories.InvoiceFactory')
    name = factory.Faker('job')
    measure = "hours"
    quantity = random.randint(1, 164)
    unit_price = random.uniform(5.5, 1000.4)
    discount = 0