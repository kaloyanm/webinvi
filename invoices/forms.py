
from django import forms
from django.forms import formset_factory
from django.utils.translation import ugettext_lazy as _

from core.mixins import TranslateLabelsFormMixin, AttrsFormMixin
from invoices.models import Invoice


class InvoiceItemForm(forms.Form):

    name = forms.CharField(required=True)
    quantity = forms.IntegerField(required=False)
    measure = forms.CharField(required=False)
    unit_price = forms.DecimalField(required=False)
    discount = forms.FloatField(required=False)

InvoiceItemFormSet = formset_factory(InvoiceItemForm)


class InvoiceForm(TranslateLabelsFormMixin, AttrsFormMixin, forms.ModelForm):

    translate_labels = {
        "client_name": _("Получател"),
        "client_city": _("Град"),
        "client_eik": _("Булстат"),
        "client_dds": _("Ин по ДДС"),
        "client_address": _("Адрес"),
        "client_mol": _("МОЛ"),
        "number": _("Номер"),
        "payment_type": _("Начин на плащане"),
        "payment_iban": _("IBAN"),
        "payment_swift": _("SWIFT"),
        "payment_bank": _("Банка"),
        "tax_base": _("Данъчна основа"),
        "dds_percent": _("ДДС"),
        "total": _("Крайна цена"),
        "accepted_by": _("Приел"),
        "created_by": _("Съставил"),
        "verbally": _("Словом"),
        "taxevent_at": _("Данъчно събитие"),
        "released_at": _("Дата на издаване"),
    }

    fields_attrs = {
        "client_name": {"class": "searchable-client"},
        "client_city": {"class": "searchable-client-fill"},
        "client_eik": {"class": "searchable-client-fill"},
        "client_dds": {"class": "searchable-client-fill"},
        "client_address": {"class": "searchable-client-fill"},
        "client_mol": {"class": "searchable-client-fill"},
        "payment_type": {"class": "searchable-invoice"},
        "payment_bank": {"class": "searchable-invoice"},
        "payment_iban": {"class": "searchable-invoice"},
        "payment_swift": {"class": "searchable-invoice"},
        "accepted_by": {"class": "searchable-invoice"},
        "created_by": {"class": "searchable-invoice"},
    }

    tax_base = forms.DecimalField(disabled=True, required=False)
    total = forms.DecimalField(disabled=True, required=False)
    verbally = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Invoice
        exclude = ('company', )
