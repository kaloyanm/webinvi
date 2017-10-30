# -*- coding: utf-8 -*-

import decimal
from django.db import models
from django.db.models import Max, Q
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres import search as pg_search
from core.models import Company, PaymentModel
from core.mixins import FillEmptyTranslationsMixin


def get_next_number(company, invoice_type):
    clauses = {"company": company}
    if invoice_type == Invoice.INVOICE_TYPE_PROFORMA:
        clauses["invoice_type"] = invoice_type
    else:
        clauses["invoice_type__in"] = [Invoice.INVOICE_TYPE_INVOICE, Invoice.INVOICE_TYPE_DEBIT,
                                       Invoice.INVOICE_TYPE_CREDIT]

    max_no = Invoice.objects.filter(**clauses).aggregate(Max('number'))\
                 .get('number__max') or 0
    return max_no + 1


# Create your models here.
class Invoice(FillEmptyTranslationsMixin, PaymentModel):

    INVOICE_TYPE_INVOICE = 'invoice'
    INVOICE_TYPE_PROFORMA = 'proforma'
    INVOICE_TYPE_CREDIT = 'credit'
    INVOICE_TYPE_DEBIT = 'debit'
    INVOICE_TYPES = (
        (INVOICE_TYPE_INVOICE, _('Фактура')),
        (INVOICE_TYPE_PROFORMA, _('Проформа')),
        (INVOICE_TYPE_CREDIT, _('Кредит')),
        (INVOICE_TYPE_DEBIT, _('Дебит')),
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

    client_eik = models.CharField(max_length=255, db_index=True)
    client_dds = models.CharField(max_length=255, null=True, blank=True)

    invoice_type = models.CharField(max_length=10, choices=INVOICE_TYPES, db_index=True, blank=False, default='invoice')
    number = models.PositiveIntegerField(db_index=True)
    ref_number = models.PositiveIntegerField(blank=True, null=True)

    released_at = models.DateField(blank=True, null=True)
    taxevent_at = models.DateField(blank=True, null=True)

    dds_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True,
                                      null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])

    note = models.TextField(blank=True, default='')
    note_tr = models.TextField(null=True)
    no_dds_reason = models.CharField(max_length=255, default='')
    no_dds_reason_tr = models.CharField(max_length=255, default='')

    currency = models.CharField(max_length=3, null=True)
    currency_rate = models.DecimalField(max_digits=10, decimal_places=6, null=True)

    search_vector = pg_search.SearchVectorField(null=True)

    class Meta:
        ordering = ("-released_at", "-invoice_type", "-number")
        unique_together = ("company", "invoice_type", "number")
        indexes = [GinIndex(fields=['search_vector'])]


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

    name = models.CharField(max_length=255, default='')
    name_tr = models.CharField(max_length=255, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.00)
    quantity = models.FloatField(blank=True, default=1)
    measure = models.CharField(max_length=55, blank=True)
    measure_tr = models.CharField(max_length=55, null=True)
    discount = models.FloatField(blank=True, null=True)
    dds_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True,
                                      null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        ordering = ('pk',)

    def __str__(self):
        return "{} - {} {}".format(self.name, self.unit_price, self.measure)

    @property
    def total(self):
        unit_price = float(self.unit_price or 0.00)
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
