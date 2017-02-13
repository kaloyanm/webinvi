from django.db import models
from django.db.models import Max
from django.conf import settings
from django.contrib.auth.models import User
from core.models import Profile

INVOICE_TYPES = (
    ('invoice', 'Invoice'),
    ('proforma', 'Proforma'),
)

# Create your models here.
class Invoice(models.Model):
    user = models.ForeignKey(User)
    receiver_name = models.CharField(max_length=255)
    receiver_eik = models.CharField(max_length=255)
    receiver_dds = models.CharField(max_length=255)
    receiver_city = models.CharField(max_length=255)
    receiver_address = models.CharField(max_length=255)
    receiver_mol = models.CharField(max_length=255)

    invoice_type = models.CharField(max_length=10, choices=INVOICE_TYPES, blank=False, default='invoice')
    invoice_no = models.PositiveIntegerField(blank=True, null=True, unique=True)
    proforma_no = models.PositiveIntegerField(blank=True, null=True, unique=True)
    released_at = models.DateField(blank=True, null=True, auto_now_add=True)
    tax_event_at = models.DateField(blank=True, null=True, auto_now_add=True)

    payment_type = models.CharField(max_length=255)
    payment_iban = models.CharField(max_length=255)
    payment_swift = models.CharField(max_length=255)
    payment_bank = models.CharField(max_length=255)

    tax_base = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)
    tax_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True, null=True)

    created_by = models.CharField(max_length=255)
    accepted_by = models.CharField(max_length=255)

    note = models.TextField()

    def __str__(self):
        return self.receiver_name

    def __pre__(self):
        return self.receiver_name

    @property
    def total(self):
        return 0

    @staticmethod
    def get_next_invoice_no():
        max_no = Invoice.objects.all().aggregate(Max('invoice_no')).get('invoice_no__max') or 0
        return max_no + 1

    @staticmethod
    def get_next_proforma_no():
        max_no = Invoice.objects.all().aggregate(Max('proforma_no')).get('proforma_no__max') or 0
        return max_no + 1

    def save(self, *args, **kwargs):
        if not self.invoice_no and self.invoice_type == 'invoice':
            self.invoice_no = self.get_next_invoice_no()
        if not self.proforma_no and self.invoice_type == 'proforma':
            self.proforma_no = self.get_next_proforma_no()

        super(Invoice, self).save(*args, **kwargs)


class InvoiceItem(models.Model):

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    name = models.CharField(max_length=155)
    quantity = models.PositiveIntegerField(blank=True)
    measure = models.CharField(max_length=55)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    discount = models.FloatField(blank=True)

    def __str__(self):
        return self.name
