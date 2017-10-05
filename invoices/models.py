# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Max
from django.utils.translation import ugettext_lazy as _

from core.models import Company




def get_next_number(company, invoice_type):
    max_no = Invoice.objects.filter(company=company, invoice_type=invoice_type) \
                 .aggregate(Max('number')) \
                 .get('number__max') or 0
    return max_no + 1


# Create your models here.
class Invoice(models.Model):

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
    client_city = models.CharField(max_length=255, default='')
    client_address = models.CharField(max_length=255, default='', db_index=True)
    client_mol = models.CharField(max_length=255, default='')

    created_by = models.CharField(max_length=255, null=True)
    accepted_by = models.CharField(max_length=255, null=True)

    payment_type = models.CharField(max_length=255, blank=True)
    payment_bank = models.CharField(max_length=255, null=True)

    client_eik = models.CharField(max_length=255, db_index=True)
    client_dds = models.CharField(max_length=255, null=True)

    invoice_type = models.CharField(max_length=10, choices=INVOICE_TYPES, blank=False, default='invoice')
    number = models.PositiveIntegerField(blank=True, null=True, db_index=True)

    released_at = models.DateField(blank=True, null=True)
    taxevent_at = models.DateField(blank=True, null=True)

    payment_iban = models.CharField(max_length=255, null=True)
    payment_swift = models.CharField(max_length=255, null=True)

    dds_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)

    note = models.TextField(null=True, default=None)
    no_dds_reason = models.CharField(max_length=255, null=True)


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
            return self.gross - (self.gross * self.dds_percent / 100)
        else:
            return self.gross

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = get_next_number(self.company, self.invoice_type)

        super(Invoice, self).save(*args, **kwargs)


class InvoiceItem(models.Model):

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    order_no = models.SmallIntegerField(blank=True)

    name = models.CharField(max_length=155, default='')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.00)
    quantity = models.FloatField(blank=True, default=1)
    measure = models.CharField(max_length=55, blank=True)
    discount = models.FloatField(blank=True, null=True)

    def __str__(self):
        return "{} - {} {}".format(self.name, self.unit_price, self.measure)

    @property
    def total(self):
        unit_price = self.unit_price if not self.discount else \
            self.unit_price - self.unit_price * self.discount * 100
        unit_price = float(unit_price)
        total = self.quantity * unit_price if self.quantity and unit_price else unit_price
        return total

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.order_no = (self.invoice.invoiceitem_set.aggregate(max=Max('order_no'))['max'] or 0) + 1
        super().save(*args, **kwargs)
