
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
)
from hvad.forms import TranslatableModelForm
from core.mixins import SubmitButtonMixin, TranslateLabelsFormMixin
from core.models import Company

User = get_user_model()

class ChangePassForm(SubmitButtonMixin, PasswordChangeForm):
    submit_button_label = _('Обнови')


class RegistratiоnForm(SubmitButtonMixin, UserCreationForm):
    submit_button_label = _('Влез')

    # Simple and elegant solution to use email as username
    class Meta:
        model = User
        fields = ["username"]
        exclude = ["email"]
    username = forms.EmailField(max_length=64)


class LoginForm(SubmitButtonMixin, AuthenticationForm):
    submit_button_label = _('Влез')


# class CompanyForm(SubmitButtonMixin, forms.Form):
#     submit_button_label = _('Запази')
#
#     name = forms.CharField(label=_('Има на компанията'))
#     eik = forms.CharField(label=_('БУЛСТАТ'))
#     dds = forms.CharField(label=_('Ин по ДДС'), required=False)
#     city = forms.CharField(label=_('Град'))
#     address = forms.CharField(label=_('Адрес'))
#     mol = forms.CharField(label=_('МОЛ'))
#     default = forms.BooleanField(required=False, label=_('Маркирай като основна'))

class CompanyForm(SubmitButtonMixin, TranslateLabelsFormMixin, TranslatableModelForm):
    translate_labels = {
        "name": _('Има на компанията'),
        "eik": _('БУЛСТАТ'),
        "dds": _('Ин по ДДС'),
        "city": _('Град'),
        "address": _('Адрес'),
        "mol": _('МОЛ'),
        "default": _('Маркирай като основна'),
    }

    class Meta:
        model = Company
        exclude = ("user", )


class CompaniesImportForm(SubmitButtonMixin, forms.Form):
    file = forms.FileField()
    wipe_existing = forms.BooleanField(required=False)


class InvoiceproImportForm(SubmitButtonMixin, forms.Form):
    file = forms.FileField()
    wipe_existing = forms.BooleanField(required=False)


class ContactForm(SubmitButtonMixin, forms.Form):
    submit_button_label = _('Изпрати')

    name = forms.CharField(label=_(u'Име'), max_length=100)
    email = forms.EmailField(label=_(u'Емейл'))
    phone = forms.CharField(widget=forms.NumberInput, label=_(u'Телефон'))
    message = forms.CharField(widget=forms.Textarea, label=_(u'Съобщение'))
