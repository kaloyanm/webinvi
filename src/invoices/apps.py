from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class InvoicesConfig(ModuleMixin, AppConfig):
    name = 'Invoices'
    icon = '<i class="mdi-communication-quick-contacts-dialer"></i>'
