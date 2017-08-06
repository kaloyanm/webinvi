from django.conf.urls import url
from invoices.views import (
    list_invoices, invoice, delete_invoice
)


urlpatterns = [
    url(r'^invoice/(?P<pk>[0-9]+)/', invoice, name='invoice'),
    url(r'^invoice/', invoice, name='invoice'),
    url(r'^proforma/(?P<pk>[0-9]+)/', invoice, {"invoice_type": "proforma"}, name='proforma'),
    url(r'^proforma/', invoice, {"invoice_type": "proforma"}, name='proforma'),
    url(r'^delete/(?P<pk>[0-9]+)', delete_invoice, name='delete'),
    url(r'^list/', list_invoices, name='list'),
]
