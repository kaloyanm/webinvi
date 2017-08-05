
from django import forms
from django.forms import formset_factory
from invoices.models import Invoice, InvoiceItem

class InvoiceItemForm(forms.Form):

    name = forms.CharField(required=True)
    quantity = forms.IntegerField(required=False)
    measure = forms.CharField(required=False)
    unit_price = forms.DecimalField(required=False)
    discount = forms.FloatField(required=False)

InvoiceItemFormSet = formset_factory(InvoiceItemForm)


class InvoiceForm(forms.ModelForm):
    
    class Meta:
        model = Invoice
        exclude = ('company', )


class SearchForm(forms.Form):
    terms = forms.CharField(min_length=4)
