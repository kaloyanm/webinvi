from django import forms
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

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


class InvoiceproImportForm(forms.Form):
    file = forms.FileField()
    wipe_existing = forms.BooleanField(required=False)


# @todo: remove it after semantic forms module is successfully installed
class ExampleSemanticForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ExampleSemanticForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'someId'
        self.helper.form_class = 'some-class'
        self.helper.form_method = 'post'
        self.helper.form_action = 'sample_form_name'

        # Note that the submit button is added separately, with a Semantic UI class.
        self.helper.add_input(Submit('submit', 'Submit', css_class='ui button'))

    like_website = forms.TypedChoiceField(
        label='Do you like this website?',
        choices=((1, 'Yes'), (0, 'No')),
        coerce=lambda x: bool(int(x)),
        widget=forms.RadioSelect,
        initial='1',
        required=True,
    )

    favorite_food = forms.CharField(
        label='What is your favorite food?',
        max_length=80,
        required=True,
    )

    favorite_color = forms.CharField(
        label='What is your favorite color?',
        max_length=80,
        required=True,
    )

    favorite_number = forms.IntegerField(
        label='Favorite number',
        required=False,
    )

    notes = forms.CharField(
        label='Additional notes or feedback',
        required=False,
    )
