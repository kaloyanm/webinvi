
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^invoices/', include('invoices.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('core.urls')),
]
