
from django import template
from django.forms import HiddenInput

register = template.Library()


@register.filter
def is_inline(field):
    return hasattr(field.field, "inline")


@register.filter
def set_hidden(field):
    setattr(field.field, 'widget', HiddenInput())
    return field


@register.filter
def disable_field(field):
    field.field.widget.attrs['readonly'] = ''
    return field
