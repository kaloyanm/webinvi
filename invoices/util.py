import uuid
import logging
from django.core.cache import cache
from django.conf import settings
from django.core.urlresolvers import reverse
from urllib.parse import urlparse, urlunparse

logger = logging.Logger(__name__)

def get_pdf_generator_url(pk, lang_code=settings.LANGUAGE_CODE):
    access_token = uuid.uuid4()
    cache.set(access_token, pk)

    if settings.PORT and settings.PORT != 80:
        port = ':' + str(settings.PORT)
    else:
        port = ''
    u = urlparse(settings.HOSTNAME)
    u = u._replace(scheme='http', netloc=settings.HOSTNAME + port)

    preview_path = reverse("printpreview", kwargs=dict(token=access_token, lang_code=lang_code))
    print_preview_url = "{}{}".format(urlunparse(u), preview_path)
    pdf_generator_url = "{}/?url={}".format(settings.PDF_SERVER, print_preview_url)
    logger.info(pdf_generator_url)
    return pdf_generator_url
