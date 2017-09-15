
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm
)

from core.mixins import SubmitButtonMixin

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


class CompanyForm(SubmitButtonMixin, forms.Form):
    submit_button_label = _('Запази')

    name = forms.CharField(label=_(u'Има на компанията'))
    eik = forms.CharField(label=_(u'БУЛСТАТ'))
    dds = forms.CharField(label=_(u'Ин по ДДС'), required=False)
    city = forms.CharField(label=_(u'Град'))
    address = forms.CharField(label=_(u'Адрес'))
    mol = forms.CharField(label=_(u'МОЛ'))
    default = forms.BooleanField(required=False, label=_(u'Маркирай като основна'))


class CompaniesImportForm(SubmitButtonMixin, forms.Form):
    file = forms.FileField()
    wipe_existing = forms.BooleanField(required=False)


class InvoiceproImportForm(SubmitButtonMixin, forms.Form):
    file = forms.FileField()
    wipe_existing = forms.BooleanField(required=False)
