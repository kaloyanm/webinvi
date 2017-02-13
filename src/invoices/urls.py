from django.conf.urls import url
from invoices.views import ListInvoice, CreateInvoice, UpdateInvoice
from invoices.views import DeleteInvoice

urlpatterns = [
    url(r'^create/(?P<invoice_type>[a-zA-Z]+)', CreateInvoice.as_view(), name='create-proforma'),
    url(r'^create/', CreateInvoice.as_view(), name='create'),
    url(r'^update/(?P<pk>[0-9]+)/(?P<invoice_type>[a-zA-Z]+)', UpdateInvoice.as_view(), name='update-proforma'),
    url(r'^update/(?P<pk>[0-9]+)', UpdateInvoice.as_view(), name='update'),
    url(r'^delete/(?P<pk>[0-9]+)', DeleteInvoice.as_view(), name='delete'),
    url(r'^list/', ListInvoice.as_view(), name='list'),
]
