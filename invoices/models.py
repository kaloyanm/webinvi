# -*- coding: utf-8 -*-

import decimal
from django.db import models
from django.db.models import Max
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _

from core.models import Company
from core.mixins import FillEmptyTranslationsMixin


def get_next_number(company, invoice_type):
    max_no = Invoice.objects.filter(company=company, invoice_type=invoice_type) \
                 .aggregate(Max('number')) \
                 .get('number__max') or 0
    return max_no + 1


# Create your models here.
class Invoice(FillEmptyTranslationsMixin, models.Model):

    INVOICE_TYPE_INVOICE = 'invoice'
    INVOICE_TYPE_PROFORMA = 'proforma'
    INVOICE_TYPE_CREDIT = 'credit'
    INVOICE_TYPE_DEBIT = 'debit'
    INVOICE_TYPES = (
        (INVOICE_TYPE_INVOICE, _('Invoice')),
        (INVOICE_TYPE_PROFORMA, _('Proforma')),
        (INVOICE_TYPE_CREDIT, _('Credit')),
        (INVOICE_TYPE_DEBIT, _('Debit')),
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    client_name = models.CharField(max_length=255, db_index=True, default='')
    client_name_tr = models.CharField(max_length=255, db_index=True, null=True)

    client_city = models.CharField(max_length=255, default='')
    client_city_tr = models.CharField(max_length=255, null=True)

    client_address = models.CharField(max_length=255, default='', db_index=True)
    client_address_tr = models.CharField(max_length=255, db_index=True, null=True)

    client_mol = models.CharField(max_length=255, default='')
    client_mol_tr = models.CharField(max_length=255, null=True)

    created_by = models.CharField(max_length=255, null=True)
    created_by_tr = models.CharField(max_length=255, null=True)

    accepted_by = models.CharField(max_length=255, null=True)
    accepted_by_tr = models.CharField(max_length=255, null=True)

    payment_type = models.CharField(max_length=255, blank=True)
    payment_type_tr = models.CharField(max_length=255, null=True)
    payment_bank = models.CharField(max_length=255, null=True)
    payment_bank_tr = models.CharField(max_length=255, null=True)

    client_eik = models.CharField(max_length=255, db_index=True)
    client_dds = models.CharField(max_length=255, null=True, blank=True)

    invoice_type = models.CharField(max_length=10, choices=INVOICE_TYPES, blank=False, default='invoice')
    number = models.PositiveIntegerField(blank=True, null=True, db_index=True)

    released_at = models.DateField(blank=True, null=True)
    taxevent_at = models.DateField(blank=True, null=True)

    payment_iban = models.CharField(max_length=255, null=True)
    payment_swift = models.CharField(max_length=255, null=True)

    dds_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True,
                                      null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])

    note = models.TextField(blank=True, default='')
    note_tr = models.TextField(null=True)
    no_dds_reason = models.CharField(max_length=255, null=True)
    no_dds_reason_tr = models.CharField(max_length=255, null=True)

    currency = models.CharField(max_length=3, null=True)
    currency_rate = models.DecimalField(max_digits=10, decimal_places=6, null=True)


    class Meta:
        ordering = ("-released_at", "-invoice_type", "-number")
        unique_together = ("company", "invoice_type", "number"),


    def __str__(self):
        return self.client_name

    def __pre__(self):
        return self.client_name

    @property
    def is_proforma(self):
        return self.invoice_type == self.INVOICE_TYPE_PROFORMA

    @property
    def gross(self):
        prices = [item.total for item in self.invoiceitem_set.all()]
        return sum(prices)

    @property
    def total(self):
        if self.dds_percent:
            return round(self.gross - (self.gross * float(self.dds_percent) / 100), 2)
        else:
            return round(self.gross, 2)


    def save(self, *args, **kwargs):
        if not self.number:
            self.number = get_next_number(self.company, self.invoice_type)

        super(Invoice, self).save(*args, **kwargs)


class InvoiceItem(FillEmptyTranslationsMixin, models.Model):

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    order_no = models.SmallIntegerField(blank=True)

    name = models.CharField(max_length=155, default='')
    name_tr = models.CharField(max_length=155, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.00)
    quantity = models.FloatField(blank=True, default=1)
    measure = models.CharField(max_length=55, blank=True)
    measure_tr = models.CharField(max_length=55, null=True)
    discount = models.FloatField(blank=True, null=True)

    def __str__(self):
        return "{} - {} {}".format(self.name, self.unit_price, self.measure)

    @property
    def total(self):
        unit_price = float(self.unit_price)
        unit_price = unit_price if not self.discount else\
            unit_price * self.discount * decimal.Decimal(100) - unit_price

        if self.quantity:
            total = unit_price * self.quantity
        else:
            total = unit_price
        return round(total, 2)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.order_no = (self.invoice.invoiceitem_set.aggregate(max=Max('order_no'))['max'] or 0) + 1
        super().save(*args, **kwargs)
