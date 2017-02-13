from django import forms
from django.utils.translation import ugettext_lazy as _
from core.models import Profile


class CompanySettingsForm(forms.ModelForm):
    provider_name = forms.CharField(label=_(u'Доставчик'))
    provider_eik = forms.CharField(label=_(u'БУЛСТАТ'))
    provider_dds = forms.CharField(label=_(u'Ин по ДДС'), required=False)
    provider_city = forms.CharField(label=_(u'Град'))
    provider_address = forms.CharField(label=_(u'Адрес'))
    provider_mol = forms.CharField(label=_(u'МОЛ'))

    class Meta:
        model = Profile
        exclude = ('user',)
