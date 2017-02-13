from django import forms
from django.forms import inlineformset_factory
from invoices.models import Invoice
from core.models import Profile

class InvoiceDetailForm(forms.Form):

    name = forms.CharField(max_length=155)
    quantity = forms.DecimalField()
    measure = forms.CharField(max_length=55)
    unit_price = forms.DecimalField()
    total = forms.DecimalField()
    discount = forms.FloatField()


class InvoiceForm(forms.ModelForm):
    PAYMENT_TYPES = (
        ('bank', 'Bank Transfer'),
    )

    receiver_name = forms.CharField()
    receiver_eik = forms.CharField(required=False)
    receiver_dds = forms.CharField(required=False)
    receiver_city = forms.CharField(required=False)
    receiver_address = forms.CharField(required=False)
    receiver_mol = forms.CharField(required=False)

    provider_name = forms.CharField(required=False)
    provider_eik = forms.CharField(required=False)
    provider_dds = forms.CharField(required=False)
    provider_city = forms.CharField(required=False)
    provider_address = forms.CharField(required=False)
    provider_mol = forms.CharField(required=False)

    invoice_no = forms.IntegerField(required=False)
    proforma_no = forms.IntegerField(required=False)
    released_at = forms.DateField(required=False)
    tax_event_at = forms.DateField(required=False)

    payment_type = forms.ChoiceField(choices=PAYMENT_TYPES)
    payment_iban = forms.CharField(required=False)
    payment_swift = forms.CharField(required=False)
    payment_bank = forms.CharField(required=False)

    tax_base = forms.DecimalField(required=False)
    tax_percent = forms.DecimalField(required=False)

    created_by = forms.CharField(required=False)
    accepted_by = forms.CharField(required=False)
    note = forms.CharField(required=False)

    class Meta:
        model = Invoice
        exclude = ['user', 'invoice_type']
