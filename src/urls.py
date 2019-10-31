from django.conf.urls import url, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin


urlpatterns = [
    url(r'^private_zone/', admin.site.urls),
    url(r'^rosetta/', include('rosetta.urls')),
]

urlpatterns += i18n_patterns(
    url(r'^invoices/', include('invoices.urls')),
    url(r'^', include('core.urls')),
    prefix_default_language=True
)
