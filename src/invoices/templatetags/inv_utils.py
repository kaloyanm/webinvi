from django import template
from django.conf import settings

register = template.Library()

def nopad(val):
    val = str(val)
    return val.rjust(10, '0')
register.filter('nopad', nopad)
