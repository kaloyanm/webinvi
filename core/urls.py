
from django.conf.urls import url
from core.views import (
    contact, home, LoginView, RegistrationView,
    logout_view, change_password, company,
    companies, drop_company, export_companies,
    import_companies, import_invoicepro, thanks,
    google_oath_login, google_auth_return)

urlpatterns = [
    url(r'^contact/', contact, name='contact'),
    url(r'^thanks/', thanks, name='thanks'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^registration/', RegistrationView.as_view(), name='registration'),
    url(r'^password/', change_password, name='password'),
    url(r'^companies/', companies, name='companies'),
    url(r'^company/drop/(?P<pk>[0-9]+)/', drop_company, name='drop_company'),
    url(r'^company/(?P<pk>[0-9]+)/', company, name='company'),
    url(r'^company/', company, name='company'),
    url(r'^export/companies/', export_companies, name='export_companies'),
    url(r'^import/companies/', import_companies, name='import_companies'),
    url(r'^import/invoicepro/', import_invoicepro, name='import_invoicepro'),

    # Gogle OAuth2 urls
    url(r'^google_login$', google_oath_login, name='google_login'),
    url(r'^google_logout$', google_oath_login, name='google_logout'),
    url(r'^oauth2callback', google_auth_return),
    # Main entry point
    url(r'^$', home, name='home'),
]
