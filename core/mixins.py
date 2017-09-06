
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class AppLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')


class SubmitButtonMixin:
    submit_button_label =  _('Запази')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'ui form'
        self.helper.add_input(Submit('submit', self.submit_button_label,
                                     css_class='ui button primary'))


class InlineFieldsMixin:

    inline_fields = []  # __all__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            if self.inline_fields[0] == "__all__" or \
                    field in self.inline_fields:
                self.fields[field].inline = True
