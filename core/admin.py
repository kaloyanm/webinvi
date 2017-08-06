from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from core.models import Company


class CompanyResource(resources.ModelResource):

    class Meta:
        model = Company
        fields = ('id', 'name', 'eik', 'dds', 'address', 'city', 'mol')

    def __init__(self, *args, **kwargs):
        if "user" in kwargs:
            self.user = kwargs["user"]
            del kwargs["user"]
        super().__init__(*args, **kwargs)

    def init_instance(self, row=None):
        instance = super().init_instance(row)
        instance.user = self.user
        return instance


class CompanyAdmin(ImportExportModelAdmin):
    resources_class = CompanyResource

# Register your models here.
# admin.site.register(Company, CompanyAdmin)
