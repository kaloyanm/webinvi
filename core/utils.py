
from django.utils.crypto import get_random_string
from django.utils import translation
from django.utils.translation import ugettext

def make_random_password(length=10,
                         allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                       'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                       '23456789'):
    """
    Generate a random password with the given length and given
    allowed_chars. The default value of allowed_chars does not have "I" or
    "O" or letters and digits that look similar -- just to avoid confusion.
    """
    return get_random_string(length, allowed_chars)


def get_translation_in(string, locale):
    translation.activate(locale)
    val = ugettext(string)
    translation.deactivate()
    return val
