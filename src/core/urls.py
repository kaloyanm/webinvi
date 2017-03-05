from django.conf.urls import url
from core.views import contact, home, LoginView, RegistrationView
from core.views import logout_view, CompanySettingsView, PasswordChangeView

urlpatterns = [
    url(r'^contact/', contact, name='contact'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^registration/', RegistrationView.as_view(), name='registration'),
    url(r'^password/', PasswordChangeView.as_view(), name='password'),
    url(r'^settings/company/', CompanySettingsView.as_view(), name='settings-company'),
    url(r'^$', home, name='home'),
]
