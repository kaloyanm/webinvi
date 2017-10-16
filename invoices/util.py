import uuid
from django.core.cache import cache
from django.conf import settings
from django.core.urlresolvers import reverse
from urllib.parse import urlparse, urlunparse


def get_pdf_generator_url(pk):
    access_token = uuid.uuid4()
    cache.set(access_token, pk)

    u = urlparse(settings.HOSTNAME)
    if u.port and u.port != 80:
        port = ':' + str(u.port)
    else:
        port = ''
    u = u._replace(scheme='http', netloc='localhost' + port)

    print_preview_url = "{}{}".format(urlunparse(u), reverse("printpreview", kwargs=dict(token=access_token)))
    pdf_generator_url = "{}/?url={}".format(settings.PDF_SERVER, print_preview_url)
    print(pdf_generator_url)
    return pdf_generator_url
