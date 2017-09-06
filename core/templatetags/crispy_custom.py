from django import template
register = template.Library()


@register.filter
def is_inline(field):
    return hasattr(field.field, "inline")

