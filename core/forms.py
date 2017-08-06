from django import forms
from django.utils.translation import ugettext_lazy as _


class CompanyForm(forms.Form):
    name = forms.CharField(label=_(u'Има на компанията'))
    eik = forms.CharField(label=_(u'БУЛСТАТ'))
    dds = forms.CharField(label=_(u'Ин по ДДС'), required=False)
    city = forms.CharField(label=_(u'Град'))
    address = forms.CharField(label=_(u'Адрес'))
    mol = forms.CharField(label=_(u'МОЛ'))
    default = forms.BooleanField(required=False, label=_(u'Маркирай като основна'))


class CompaniesImportForm(forms.Form):
    file = forms.FileField()
    wipe_existing = forms.BooleanField(required=False)
