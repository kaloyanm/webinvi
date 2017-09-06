
from modeltranslation.translator import translator, TranslationOptions
from invoices.models import Invoice, InvoiceItem


class InvoiceTranslationOptions(TranslationOptions):
    fields = (
        "client_name",
        "client_city",
        "client_address",
        "client_mol",
    )


class InvoiceItemTOptions(TranslationOptions):
    fields = ("name", "measure")

translator.register(Invoice, InvoiceTranslationOptions)
translator.register(InvoiceItem, InvoiceItemTOptions)
