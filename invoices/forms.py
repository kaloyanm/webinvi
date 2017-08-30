
from django import forms
from django.forms import formset_factory
from invoices.models import Invoice, InvoiceItem
from core.mixins import InjectCssClassMixin

class InvoiceItemForm(forms.Form):

    name = forms.CharField(required=True)
    quantity = forms.IntegerField(required=False)
    measure = forms.CharField(required=False)
    unit_price = forms.DecimalField(required=False)
    discount = forms.FloatField(required=False)

InvoiceItemFormSet = formset_factory(InvoiceItemForm)


class InvoiceForm(InjectCssClassMixin, forms.ModelForm):
    css_classes = {
        "client_eik": "inline field custom-inline",
    }

    class Meta:
        model = Invoice
        exclude = ('company', )


class SearchForm(forms.Form):
    terms = forms.CharField(min_length=4)
