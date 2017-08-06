from django.contrib import admin
from invoices.models import Invoice


class InvoiceAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

# Register your models here.
# admin.site.register(Invoice, InvoiceAdmin)
