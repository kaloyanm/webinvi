
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button


class SemanticUIFormMixin:
    submit_button_label = _('Запази')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'ui form'

        if hasattr(self, 'instance') and self.instance.pk:
            self.helper.add_input(Button('delete', _('Delete'), css_class='ui button red', css_id='delete-button'))
        self.helper.add_input(Submit('submit', self.submit_button_label, css_class='ui button primary'))


class InlineFieldsMixin:

    inline_fields = []  # __all__

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            if self.inline_fields[0] == "__all__" or \
                    field in self.inline_fields:
                self.fields[field].inline = True


class TranslateLabelsFormMixin:
    translate_labels = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field, label in self.translate_labels.items():
            if field not in self.fields.keys():
                raise ImproperlyConfigured
            self.fields[field].label = label


class AttrsFormMixin:
    fields_attrs = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field, attrs in self.fields_attrs.items():
            if field not in self.fields.keys():
                raise ImproperlyConfigured
            self.fields[field].widget.attrs.update(attrs)


class FillEmptyTranslationsMixin:
    def save(self, *args, **kwargs):
        # update the second language from the base if it is empty
        for _field in self._meta.get_fields():
            if _field.name.endswith('_tr') and not getattr(self, _field.name):
                setattr(self, _field.name, getattr(self, _field.name.replace('_tr', '')))
        super(FillEmptyTranslationsMixin, self).save(*args, **kwargs)


class OffRequiredFieldsMixin:
    off_required_fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.off_required_fields:
            if field not in self.fields.keys():
                raise ImproperlyConfigured
            self.fields[field].required = False
