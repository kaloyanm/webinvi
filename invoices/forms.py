
from django import forms
from django.forms import formset_factory
from django.utils.translation import ugettext_lazy as _

from core.mixins import TranslateLabelsFormMixin, AttrsFormMixin, OffRequiredFieldsMixin
from core.business_settings import NO_DDS_REASONS
from invoices.models import Invoice


class InvoiceItemForm(forms.Form):

    id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    name = forms.CharField(required=False)
    name_tr = forms.CharField(required=False)
    quantity = forms.IntegerField(required=False)
    measure = forms.CharField(required=False)
    measure_tr = forms.CharField(required=False)
    unit_price = forms.DecimalField(required=False)
    discount = forms.FloatField(required=False)

InvoiceItemFormSet = formset_factory(InvoiceItemForm, can_delete=True)

class InvoiceForm(TranslateLabelsFormMixin, AttrsFormMixin,
                  OffRequiredFieldsMixin, forms.ModelForm):

    translate_labels = {
        "client_name": _("Получател"),
        "client_name_tr": _("Получател"),
        "client_city": _("Град"),
        "client_city_tr": _("Град"),
        "client_eik": _("Булстат"),
        "client_dds": _("Ин по ДДС"),
        "client_address": _("Адрес"),
        "client_address_tr": _("Адрес"),
        "client_mol": _("МОЛ"),
        "client_mol_tr": _("МОЛ"),
        "number": _("Номер"),
        "payment_type": _("Начин на плащане"),
        "payment_iban": _("IBAN"),
        "payment_swift": _("SWIFT"),
        "payment_bank": _("Банка"),
        "dds_percent": _("ДДС"),
        "accepted_by": _("Приел"),
        "accepted_by_tr": _("Приел"),
        "created_by": _("Съставил"),
        "created_by_tr": _("Съставил"),
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
        "no_dds_reason": {"class": "ui search dropdown"}
    }

    off_required_fields = [
        'client_name_tr',
        'client_address_tr',
        'client_city_tr',
        'client_mol_tr',
        'payment_type_tr',
        'payment_bank_tr',
        'created_by_tr',
        'accepted_by_tr',
        'note_tr',
        'no_dds_reason_tr',
    ]

    no_dds_reason = forms.ChoiceField(required=False, choices=NO_DDS_REASONS)
    verbally = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Invoice
        exclude = []


    def clean(self):
        cleaned_data = super().clean()
        invoice_number = cleaned_data.get('number')
        company = cleaned_data.get('company')
        invoice_type = cleaned_data.get('invoice_type')
        qry = Invoice.objects.filter(company=company, number=invoice_number, invoice_type=invoice_type)

        if self.instance and self.instance.pk:
            qry = qry.exclude(pk=self.instance.pk)

        if qry.exists():
            self.add_error("number", _("The number already exists.".format(invoice_number)))
