
from django.http import HttpResponse
from django.conf import settings


class ForceDefaultLanguageMiddleware:
    """
    Ignore Accept-Language HTTP headers

    This will force the I18N machinery to always choose settings.LANGUAGE_CODE
    as the default initial language, unless another one is set via sessions or cookies

    Should be installed *before* any middleware that checks request.META['HTTP_ACCEPT_LANGUAGE'],
    namely django.middleware.locale.LocaleMiddleware
    """

    def process_request(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']


class ForceUsernameEmail:
    """
    The system uses username to keep the mail so the real email field is not much used
    """
    def process_request(self, request):
        if hasattr(request, 'user') and request.user:
            request.user.email = request.user.username
