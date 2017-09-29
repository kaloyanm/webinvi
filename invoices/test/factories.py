# -*- coding: utf-8 -*-

import factory
import datetime

from django.utils.translation import ugettext_lazy as _
from factory import fuzzy
from invoices.models import Invoice, InvoiceItem

class InvoiceFactory(factory.DjangoModelFactory):
    class Meta:
        model = Invoice

    company = factory.SubFactory("core.test.factories.CompanyFactory")
    client_name = factory.Faker('company', locale='bg_BG')
    client_eik = factory.Sequence(lambda n: 2345678912 - n) # any ten digits number would suffice
    client_city = factory.Faker('city', locale='bg_BG')
    client_address = factory.Faker('address', locale='bg_BG')
    client_mol = factory.Faker('name', locale='bg_BG')

    invoice_type = fuzzy.FuzzyChoice(['invoice', 'proforma'])
    released_at = factory.Faker('date_time_between_dates',
        datetime_start = datetime.datetime(2014, 1, 1),
        datetime_end = datetime.datetime(2017, 1, 1, 20)
    )
    taxevent_at = factory.Faker('date_time_between_dates',
        datetime_start = datetime.datetime(2014, 1, 1),
        datetime_end = datetime.datetime(2017, 1, 1, 20)
    )

    payment_type = fuzzy.FuzzyChoice(["Wire transfer"])
    payment_bank = factory.Faker('company')


class InvoiceItemFactory(factory.DjangoModelFactory):
    class Meta:
        model = InvoiceItem

    invoice = factory.SubFactory('invoices.test.factories.InvoiceFactory')
    name = factory.Faker('job', locale='bg_BG')
    measure = fuzzy.FuzzyChoice(["hours", "weeks"])
    quantity = fuzzy.FuzzyInteger(1, 164)
    unit_price = fuzzy.FuzzyFloat(5.5, 1000.4)
    discount = 0
