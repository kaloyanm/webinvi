from django import template

register = template.Library()

def nopad(val):
    val = str(val)
    return val.rjust(10, '0')


@register.filter(name='nopad')
def _nopad(val):
    return nopad(val)


@register.filter
def strike(val, apply=False):
    if apply:
        t = template.Template("<strike>{{message}}</strike>")
        val = t.render(template.Context({"message":val}))
    return val
