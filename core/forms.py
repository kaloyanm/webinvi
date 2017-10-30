
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
)
from core.mixins import SemanticUIFormMixin, TranslateLabelsFormMixin, OffRequiredFieldsMixin
from core.models import Company

User = get_user_model()

class ChangePassForm(SemanticUIFormMixin, PasswordChangeForm):
    submit_button_label = _('Обнови')


class RegistrationForm(SemanticUIFormMixin, UserCreationForm):
    submit_button_label = _('Влез')

    # Simple and elegant solution to use email as username
    class Meta:
        model = User
        fields = ["username"]
        exclude = ["email"]
    username = forms.EmailField(max_length=64, label=_("Email"))


class LoginForm(SemanticUIFormMixin, AuthenticationForm):
    submit_button_label = _('Влез')


class CompanyForm(SemanticUIFormMixin, TranslateLabelsFormMixin, OffRequiredFieldsMixin,
                  forms.ModelForm):
    translate_labels = {
        "name": _('Имe на компанията'),
        "name_tr": _('Имe на компанията'),
        "eik": _('БУЛСТАТ'),
        "dds": _('Ин по ДДС'),
        "city": _('Град'),
        "city_tr": _('Град'),
        "address": _('Адрес'),
        "address_tr": _('Адрес'),
        "mol": _('МОЛ'),
        "mol_tr": _('МОЛ'),
        "payment_type": _("Начин на плащане"),
        "payment_type_tr": _("Начин на плащане"),
        "payment_iban": _("IBAN"),
        "payment_swift": _("SWIFT/BIC"),
        "payment_bank": _("Банка"),
        "payment_bank_tr": _("Банка"),
    }

    off_required_fields = ['payment_type', 'payment_type_tr', 'payment_iban', 'payment_swift', 'payment_bank', 'payment_bank_tr',
                           'name_tr', 'city_tr', 'address_tr', 'mol_tr']

    class Meta:
        model = Company
        exclude = ("user",)


class InvoiceproImportForm(SemanticUIFormMixin, forms.Form):
    file = forms.FileField()
    import_type = forms.ChoiceField(required=True, choices=(
        ('invoices', _('Компании и фактури')),
        ('companies', _('Компании')),
    ))
    wipe_existing = forms.BooleanField(required=False, label=_("Изтрий съществуващите"))


class ContactForm(SemanticUIFormMixin, forms.Form):
    submit_button_label = _('Изпрати')

    name = forms.CharField(label=_(u'Име'), max_length=100)
    email = forms.EmailField(label=_(u'Емейл'))
    phone = forms.CharField(widget=forms.NumberInput, label=_(u'Телефон'))
    message = forms.CharField(widget=forms.Textarea, label=_(u'Съобщение'))
