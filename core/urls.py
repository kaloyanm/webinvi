
from django.conf.urls import url
from django.views import defaults as default_views
from django.conf import settings
from core.views import (
    contact, home, LoginView, RegistrationView,
    logout_view, change_password, company,
    companies, drop_company, import_invoicepro, thanks,
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
    url(r'^import/invoicepro/', import_invoicepro, name='import_invoicepro'),

    # Gogle OAuth2 urls
    url(r'^google_login$', google_oath_login, name='google_login'),
    url(r'^google_logout$', google_oath_login, name='google_logout'),
    url(r'^oauth2callback', google_auth_return),
    # Main entry point
    url(r'^$', home, name='home'),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
