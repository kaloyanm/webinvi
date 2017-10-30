from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from core.models import Company
from invoices.models import Invoice, InvoiceItem


class CompanyResource(resources.ModelResource):

    class Meta:
        model = Company
        import_id_fields = ('eik', )
        fields = ('name', 'eik', 'dds', 'address', 'city', 'mol', 'user')


class InvoiceResource(resources.ModelResource):

    class Meta:
        model = Invoice
        import_id_fields = ('invoice_type', 'number', 'company')
        fields = (
            'client_name',
            'client_city',
            'client_address',
            'client_mol',

            'created_by',
            'accepted_by',

            'payment_type',
            'payment_bank',

            'client_eik',
            'client_dds',

            'invoice_type',
            'number',

            'released_at',
            'taxevent_at',

            'payment_iban',
            'payment_swift',

            'dds_percent',

            'note',
            'no_dds_reason',

            'company',
        )


class InvoiceItemResource(resources.ModelResource):

    class Meta:
        model = InvoiceItem
        import_id_fields = ('invoice', 'order_no')
        fields = (
            'invoice',
            'order_no',

            'name',
            'unit_price',
            'quantity',
            'measure',
            'discount',
        )


class CompanyAdmin(ImportExportModelAdmin):
    resources_class = CompanyResource

# Register your models here.
# admin.site.register(Company, CompanyAdmin)
