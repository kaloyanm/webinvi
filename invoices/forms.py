from django import forms
from django.forms import formset_factory
from django.utils.translation import ugettext_lazy as _

from core.mixins import TranslateLabelsFormMixin, AttrsFormMixin, OffRequiredFieldsMixin
from invoices.models import Invoice


class InvoiceItemForm(forms.Form):

    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    name = forms.CharField(required=False)
    quantity = forms.IntegerField(required=False)
    measure = forms.CharField(required=False)
    unit_price = forms.DecimalField(required=False)
    discount = forms.FloatField(required=False)


InvoiceItemFormSet = formset_factory(InvoiceItemForm, can_delete=True)


class InvoiceForm(TranslateLabelsFormMixin, AttrsFormMixin,
                  forms.ModelForm):

    translate_labels = {
        "client_name": _("Получател"),
        "client_city": _("Град"),
        "client_eik": _("БУЛСТАТ"),
        "client_dds": _("Ин по ДДС"),
        "client_address": _("Адрес"),
        "client_mol": _("МОЛ"),
        "number": _("Номер"),
        "payment_type": _("Начин на плащане"),
        "payment_iban": _("IBAN"),
        "payment_swift": _("SWIFT/BIC"),
        "payment_bank": _("Банка"),
        "dds_percent": _("ДДС"),
        "accepted_by": _("Приел"),
        "created_by": _("Съставил"),
        "verbally": _("Словом"),
        "taxevent_at": _("Данъчно събитие"),
        "no_dds_reason": _("Основание за неначисляване на ДДС"),
    }

    fields_attrs = {
        "client_name": {"class": "searchable-client"},
        "client_city": {"class": "searchable-client-fill"},
        "client_eik": {"class": "searchable-client-fill"},
        "client_dds": {"class": "searchable-client-fill"},
        "client_address": {"class": "searchable-client-fill"},
        "client_mol": {"class": "searchable-client-fill"},
        "no_dds_reason": {"class": "searchable-invoice"},
        "payment_bank": {"class": "searchable-invoice"},
        "payment_type": {"class": "searchable-invoice"},
        "payment_iban": {"class": "searchable-invoice"},
        "payment_swift": {"class": "searchable-invoice"},
        "accepted_by": {"class": "searchable-invoice"},
        "created_by": {"class": "searchable-invoice"},
    }

    no_dds_reason = forms.CharField(required=False, initial='Чл. 113, ал.9 от ЗДДС')
    verbally = forms.CharField(max_length=255, required=False)
    # currency = forms.CharField(required=False)
    # currency_rate = forms.DecimalField(required=False)

    class Meta:
        model = Invoice
        exclude = ['search_vector', 'deleted']

    def clean(self):
        cleaned_data = super().clean()
        # if 'currency' in cleaned_data and not cleaned_data['currency']:
        #     del cleaned_data['currency']
        #
        # if 'currency_rate' in cleaned_data and not cleaned_data['currency_rate']:
        #     del cleaned_data['currency_rate']
        invoice_number = cleaned_data.get('number')
        invoice_type = cleaned_data.get('invoice_type')
        qry = Invoice.objects.filter(number=invoice_number, invoice_type=invoice_type)

        if self.instance and self.instance.pk:
            qry = qry.exclude(pk=self.instance.pk)

        if qry.exists():
            self.add_error("number", _("Номерът вече съществува."))
