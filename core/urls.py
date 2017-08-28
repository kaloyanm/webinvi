
from django.conf.urls import url
from core.views import (profile,
    contact, home, LoginView, RegistrationView,
    logout_view, change_password, company,
    companies, drop_company, export_companies,
    import_companies, import_invoicepro, collaborators,
    invite, drop_collab, verify_collab)

urlpatterns = [
    url(r'^profile/', profile, name='profile'),
    url(r'^contact/', contact, name='contact'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^registration/', RegistrationView.as_view(), name='registration'),
    url(r'^password/', change_password, name='password'),
    url(r'^companies/', companies, name='companies'),
    url(r'^company/drop/(?P<pk>[0-9]+)/', drop_company, name='drop_company'),
    url(r'^company/(?P<pk>[0-9]+)/', company, name='company'),
    url(r'^collaborators/invite/(?P<company_pk>[0-9]+)/', invite, name='invite'),
    url(r'^collaborators/drop/(?P<pk>[0-9]+)/', drop_collab, name='drop_collab'),
    url(r'^collaborators/verify/(?P<key>[A-Z0-9]+)/', verify_collab, name='verify_collab'),
    url(r'^collaborators/(?P<company_pk>[0-9]+)/', collaborators, name='collaborators'),
    url(r'^company/', company, name='company'),
    url(r'^export/companies/', export_companies, name='export_companies'),
    url(r'^import/companies/', import_companies, name='import_companies'),
    url(r'^import/invoicepro/', import_invoicepro, name='import_invoicepro'),

    # Main entry point
    url(r'^$', home, name='home'),
]
