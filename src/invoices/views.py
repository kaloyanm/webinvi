
# from django.shortcuts import render
import json

from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.forms.models import model_to_dict

from .forms import InvoiceForm, InvoiceDetailForm
from .models import Invoice, InvoiceItem
from .templatetags.inv_utils import nopad
from core.mixins import AppLoginRequiredMixin


def get_invoice_details(request):
    '''
    Helper method to get invoice items from the form
    '''
    invoice_details_prefix = 'invoice_details[{}]'
    invoice_details_fields = ['name', 'quantity', 'measure', 'unit_price', 'discount', 'total']

    details = {}
    for field in invoice_details_fields:
        post_field_key = invoice_details_prefix.format(field)
        details[field] = request.POST.getlist(post_field_key)

    # create empty table values
    longest = len(max(details.values()))
    default_row = dict(zip(invoice_details_fields, [''] * len(invoice_details_fields)))
    invoice_details = [default_row.copy() for _ in range(longest)]

    # update the columns
    for column, data in details.items():
        row_index = 0
        for value in data:
            invoice_details[row_index][column] = value
            row_index += 1
    return invoice_details


# Create your views here.
class ListInvoice(AppLoginRequiredMixin, generic.ListView):
    model = Invoice
    context_object_name = 'invoices_list'


class CreateInvoice(AppLoginRequiredMixin, generic.CreateView):
    form_class = InvoiceForm
    success_url = reverse_lazy('list')
    template_name = 'invoices/invoice_form.html'

    def __init__(self, *args, **kwargs):
        super(CreateInvoice, self).__init__(*args, **kwargs)
        self.object = None
        self.invoice_type = 'invoice' # default
        self.invoice_details = []

    def get(self, request, invoice_type='invoice', **kwargs):
        self.invoice_type = invoice_type
        return super(CreateInvoice, self).get(request, invoice_type, **kwargs)

    def post(self, request, invoice_type='invoice', **kwargs):
        self.invoice_details = get_invoice_details(request)
        self.invoice_type = invoice_type

        invalid_forms = []
        valid_forms = []
        for item in self.invoice_details:
            item_form = InvoiceDetailForm(item)
            if not item_form.is_valid():
                invalid_forms.append(item_form)
            else:
                valid_forms.append(item_form)

        form = self.get_form(self.form_class)

        if form.is_valid() and len(invalid_forms) == 0:
            return self.form_valid(form, valid_forms)
        else:
            return self.form_invalid(form, invalid_forms)

    def get_context_data(self, **kwargs):
        context = super(CreateInvoice, self).get_context_data(**kwargs)
        context['invoice_type'] = self.invoice_type
        context['invoice_details'] = self.invoice_details
        context['invoice_details_json'] = json.dumps(self.invoice_details)
        return context

    def form_valid(self, form, valid_forms):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.invoice_type = self.invoice_type
        self.object.save()

        if len(valid_forms) > 0:
            for form_entry in valid_forms:
                inv_item = InvoiceItem(**form_entry.cleaned_data)
                inv_item.invoice = self.object
                inv_item.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, invalid_forms):
        return self.render_to_response(self.get_context_data(form=form, invalid_forms=invalid_forms))

    def get_initial(self):
        initial = super().get_initial()
        initial.update(model_to_dict(self.request.user.profile))
        initial['invoice_no'] = nopad(Invoice.get_next_invoice_no())
        initial['proforma_no'] = nopad(Invoice.get_next_proforma_no())
        return initial


class UpdateInvoice(AppLoginRequiredMixin, generic.edit.UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoices/invoice_form.html'

    def get_success_url(self):
        return reverse_lazy('update', kwargs={'pk': self.object.pk})

    def get_context_data(self):
        context = super(UpdateInvoice, self).get_context_data()
        context['object'] = self.object

        items = self.object.invoiceitem_set.all().values()
        items = items if items else {} # [] is not serializible

        context['invoice_details'] = items
        context['invoice_details_json'] = json.dumps(items)
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial.update(model_to_dict(self.request.user.profile))
        return initial


class DeleteInvoice(AppLoginRequiredMixin, generic.edit.DeleteView):
    model = Invoice

    def get_success_url(self):
        return reverse_lazy('list')

