import uuid
from django.core.cache import cache
from django.conf import settings
from django.core.urlresolvers import reverse


def get_pdf_generator_url(pk):
    access_token = uuid.uuid4()
    cache.set(access_token, pk)

    print_preview_url = "{}{}".format(settings.HOSTNAME, reverse("printpreview", kwargs=dict(token=access_token)))
    pdf_generator_url = "{}/?url={}".format(settings.PDF_SERVER, print_preview_url)

    return pdf_generator_url
