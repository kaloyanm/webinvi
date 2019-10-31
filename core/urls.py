
from django.conf.urls import url
from django.views import defaults as default_views
from django.conf import settings
from core.views import (
    contact, home, LoginView, registration,
    logout_view, change_password, company,
    thanks, ResetView, ResetDoneView, RecoverView, RecoverDoneView)


urlpatterns = [
    url(r'^contact/', contact, name='contact'),
    url(r'^thanks/', thanks, name='thanks'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^registration/', registration, name='registration'),
    url(r'^company/', company, name='company'),

    # recover password
    url(r'^password/recover/done/(?P<signature>.+)/$', RecoverDoneView.as_view(), name='password_reset_sent'),
    url(r'^password/recover/$', RecoverView.as_view(), name='password_reset_recover'),
    url(r'^password/reset/done/$', ResetDoneView.as_view(), name='password_reset_done'),
    url(r'^password/reset/(?P<token>[\w:-]+)/$', ResetView.as_view(), name='password_reset_reset'),

    # when logged i n
    url(r'^password/', change_password, name='password'),
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
