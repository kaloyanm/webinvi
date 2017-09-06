# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Max
from core.models import Company


INVOICE_TYPES = (
    ('invoice', 'Invoice'),
    ('proforma', 'Proforma'),
)


def get_next_number(company, invoice_type):
    max_no = Invoice.objects.filter(company=company, invoice_type=invoice_type) \
                 .aggregate(Max('number')) \
                 .get('number__max') or 0
    return max_no + 1


# Create your models here.
class Invoice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    client_name = models.CharField(max_length=255, db_index=True)
    client_eik = models.CharField(max_length=255, db_index=True)
    client_dds = models.CharField(max_length=255, blank=True)
    client_city = models.CharField(max_length=255)
    client_address = models.CharField(max_length=255, db_index=True)
    client_mol = models.CharField(max_length=255)

    invoice_type = models.CharField(max_length=10, choices=INVOICE_TYPES, blank=False, default='invoice')
    number = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    released_at = models.DateField(blank=True, null=True)
    taxevent_at = models.DateField(blank=True, null=True)

    payment_type = models.CharField(max_length=255, blank=True)
    payment_iban = models.CharField(max_length=255, blank=True)
    payment_swift = models.CharField(max_length=255, blank=True)
    payment_bank = models.CharField(max_length=255, blank=True)

    dds_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)

    created_by = models.CharField(max_length=255, blank=True)
    accepted_by = models.CharField(max_length=255, blank=True)

    note = models.TextField()
    no_dds_reason = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ("-released_at", "-invoice_type", "-number")
        unique_together = ("company", "invoice_type", "number"),


    def __str__(self):
        return self.client_name

    def __pre__(self):
        return self.client_name

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
    name = models.CharField(max_length=155)
    quantity = models.FloatField(blank=True, default=1)
    measure = models.CharField(max_length=55, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
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
