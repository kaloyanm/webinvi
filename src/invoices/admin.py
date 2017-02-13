from django.contrib import admin
from invoices.models import Invoice


# class InvoiceImportAdmin(admin.ModelAdmin):
#     fields = ['supplied_file']
# 
# 
# class InvoiceItemsInline(admin.StackedInline):
#     model = InvoiceItem


class InvoiceAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

# Register your models here.
admin.site.register(Invoice, InvoiceAdmin)
