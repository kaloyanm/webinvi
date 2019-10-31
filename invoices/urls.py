from django.conf.urls import url
from invoices.views import (
    list_invoices, invoice_details, delete_invoice, print_preview, print_invoice,
    autocomplete_field, autocomplete_client, change_invoice_language,
    proforma2invoice, invoice2announce
)


urlpatterns = [
    url(r'^printpreview/(?P<token>[a-zA-Z0-9\-]+)/(?P<lang_code>[a-zA-Z]+)/', print_preview, name='printpreview'),
    url(r'^print/(?P<pk>[0-9]+)/', print_invoice, name='print'),
    url(r'^invoice_details/(?P<pk>[0-9]+)/', invoice_details, name='invoice'),
    url(r'^invoice_details/', invoice_details, name='invoice'),
    url(r'^proforma_details/(?P<pk>[0-9]+)/', invoice_details, {"invoice_type": "proforma"}, name='proforma'),
    url(r'^proforma_details/', invoice_details, {"invoice_type": "proforma"}, name='proforma'),
    url(r'^credit_details/(?P<pk>[0-9]+)/', invoice_details, {"invoice_type": "credit"}, name='credit'),
    url(r'^debit_details/(?P<pk>[0-9]+)/', invoice_details, {"invoice_type": "debit"}, name='debit'),
    url(r'^announce_details/(?P<pk>[0-9]+)/(?P<announce_type>[a-z]+)/', invoice2announce, name='announce'),
    url(r'^convert/proforma/(?P<pk>[0-9]+)/', proforma2invoice, name='convert_proforma'),
    url(r'^delete/(?P<pk>[0-9]+)/', delete_invoice, name='delete'),
    url(r'^list_invoices/(?P<company_pk>[0-9]+)/', list_invoices, name='list_invoices'),
    url(r'^list_invoices/', list_invoices, name='list_invoices'),
    url(r'^change_lang/(?P<pk>[0-9]+)/(?P<lang>[a-zA-Z]+)/', change_invoice_language, name='change_lang'),
    url(r'^autocomplete/client/', autocomplete_client, name='autocomplete_client'),
    url(r'^autocomplete/', autocomplete_field, name='autocomplete'),
]
