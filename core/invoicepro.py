from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect, render

from invoices.models import Invoice
from core.models import Company
from core.forms import InvoiceproImportForm
from core.import_export.invoicepro import read_invoicepro_file, InvoiceProForeignKey, InvoiceProPaymentType, InvoiceProDocumentType, ImportException
from core.admin import CompanyResource, InvoiceResource, InvoiceItemResource
import logging

logger = logging.getLogger(__name__)


def dump_import_errors(result):
    import traceback
    import sys
    logger.error(result.base_errors)
    for e in result.row_errors():
        logger.error(traceback.format_exception(None,
                     e[1][0].error, e[1][0].error.__traceback__),
                     file=sys.stderr, flush=True)


@login_required
def import_invoicepro(request):
    form = InvoiceproImportForm()

    if request.method == "POST":
        form = InvoiceproImportForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                invoicepro_file = read_invoicepro_file(request.FILES["file"])
                companies_dataset = invoicepro_file['companies'].as_dataset({
                    'Name_bg': 'name',
                    'Bulstat': 'eik',
                    'VatId': 'dds',
                    'Address_bg': 'address',
                    'City_bg': 'city',
                    'Mol_bg': 'mol',
                })
                company_resource = CompanyResource(user=request.user)
                company_import_result = company_resource.import_data(companies_dataset, dry_run=False)
                if company_import_result.has_errors():
                    dump_import_errors(company_import_result)
                    raise ImportException()

                if form.cleaned_data['import_type'] == 'invoices':
                    for row_result in company_import_result.rows:
                        # find the invoicepro company id from out database id
                        company = Company.objects.get(pk=row_result.object_id)
                        invoice_pro_company_records = invoicepro_file['companies'].filter(Bulstat=company.eik)
                        invoice_pro_company_id = invoice_pro_company_records.get_value('id', 0)
                        # print('Import invoices for {} {}'.format(company, invoice_pro_company_id))
                        # Prepare import dataset
                        invoicepro_invoices = invoicepro_file['invoices'].filter(CompanyId=invoice_pro_company_id)
                        invoices_dataset = invoicepro_invoices.append_column({'company': company.id}).as_dataset({
                            InvoiceProForeignKey(invoicepro_file['partners'], 'PartnerId', 'id', 'Name_bg'): 'client_name',
                            InvoiceProForeignKey(invoicepro_file['partners'], 'PartnerId', 'id', 'City_bg'): 'client_city',
                            InvoiceProForeignKey(invoicepro_file['partners'], 'PartnerId', 'id', 'Address_bg'): 'client_address',
                            InvoiceProForeignKey(invoicepro_file['partners'], 'PartnerId', 'id', 'Mol_bg'): 'client_mol',
                            #
                            'Compiler': 'created_by',
                            'Recipient': 'accepted_by',
                            #
                            InvoiceProPaymentType('PaymentMethodId'): 'payment_type',
                            InvoiceProForeignKey(invoicepro_file['companies_bank_accounts'], 'BankAccId', 'id', 'BankName'): 'payment_bank',
                            #
                            InvoiceProForeignKey(invoicepro_file['partners'], 'PartnerId', 'id', 'Bulstat'): 'client_eik',
                            InvoiceProForeignKey(invoicepro_file['partners'], 'PartnerId', 'id', 'VatId'): 'client_dds',
                            #
                            InvoiceProDocumentType('DocumentType'): 'invoice_type',
                            'DocNr': 'number',
                            #
                            'DateCreate': 'released_at',
                            'DateEvent': 'taxevent_at',
                            #
                            InvoiceProForeignKey(invoicepro_file['companies_bank_accounts'], 'BankAccId', 'id', 'Iban'): 'payment_iban',
                            InvoiceProForeignKey(invoicepro_file['companies_bank_accounts'], 'BankAccId', 'id', 'Bic'): 'payment_swift',
                            #
                            'TotalVat': 'dds_percent',
                            #
                            'DealDescription': 'note',
                            'NoVatReason': 'no_dds_reason',
                            'company': 'company',
                        })
                        # print(invoices_dataset)
                        # Run import
                        invoice_resource = InvoiceResource()
                        invoice_import_result = invoice_resource.import_data(invoices_dataset, dry_run=False)
                        if invoice_import_result.has_errors():
                            dump_import_errors(invoice_import_result)
                            raise ImportException()
                        document_type_lookup = InvoiceProDocumentType('dummy')
                        for row_result in invoice_import_result.rows:
                            # find invoicepro invoice id from our database id
                            invoice = Invoice.objects.get(pk=row_result.object_id)
                            invoice_pro_invoice_records = invoicepro_invoices.filter(DocNr=f'{invoice.number:010d}', DocumentType=document_type_lookup.reverse_lookup(invoice.invoice_type))
                            invoice_pro_invoice_id = invoice_pro_invoice_records.get_value('id', 0)
                            # Prepare dataset for import
                            invoice_items_records = invoicepro_file['invoice_items'].filter(DocumentId=invoice_pro_invoice_id)
                            invoice_items_dataset = invoice_items_records.append_column({'invoice': invoice.id}).as_dataset({
                                'No': 'order_no',

                                'Name_bg': 'name',
                                'Price': 'unit_price',
                                'Quantity': 'quantity',
                                InvoiceProForeignKey(invoicepro_file['measures'], 'Measure', 'id', 'Name_bg'): 'measure',
                                'Discount': 'discount',
                                'invoice': 'invoice',

                            })
                            # print(invoice_items_dataset)
                            invoice_item_resource = InvoiceItemResource()
                            invoice_items_import_result = invoice_item_resource.import_data(invoice_items_dataset, dry_run=False)

                            if invoice_items_import_result.has_errors():
                                dump_import_errors(invoice_items_import_result)
                                raise ImportException()
                return redirect(reverse_lazy("list"))
            except ImportException as e:
                logger.exception('Import Exception')
                raise Http404

    return render(request, template_name="core/_import_invoicepro.html",
                  context={"form": form})
