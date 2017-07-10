# -*- coding: utf-8 -*-

import json

from django.db import transaction
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator


from core.forms import CompanyForm
from invoices.forms import InvoiceForm, InvoiceItemFormSet
from invoices.models import (
    Invoice,
    InvoiceItem,
    get_next_invoice_no,
    get_next_proforma_no,
)


def django_json_dumps(items):
    return json.dumps(items, cls=DjangoJSONEncoder)


def process_invoice(request, form, form_items):
    if form.is_valid() and form_items.is_valid():
        instance = form.save()
        instance.company = request.company
        instance.save()

        with transaction.atomic():
            instance.invoiceitem_set.all().delete()
            for form in form_items:
                invoiceitem = InvoiceItem(**form.cleaned_data)
                invoiceitem.invoice = instance
                invoiceitem.company = request.company
                invoiceitem.save()
        return True
    return False

@login_required
def invoice(request, pk=None, invoice_type="invoice"):
    if pk:
        try:
            instance = get_object_or_404(Invoice, pk=pk)
        except Invoice.DoesNotExist:
            pass
    else:
        instance = None

    default_data = {
        "invoice_no": get_next_invoice_no(request.company),
        "proforma_no": get_next_proforma_no(request.company),
        "released_at": str(timezone.now()),
        "taxevent_at": str(timezone.now()),
    }

    context = {
        "form": InvoiceForm(initial=default_data),
        "formset": json.dumps({}),
        "invoice_type": invoice_type,
        "company_form": CompanyForm(model_to_dict(request.company)),
        "pk": pk,
    }

    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=instance)
        form_items = InvoiceItemFormSet(request.POST)

        if process_invoice(request, form, form_items):
            return redirect(reverse(invoice_type, args=[pk]))

        context["form"] = form
    else:
        if instance:
            context["company_form"] = CompanyForm(initial=model_to_dict(instance.company))
            context["form"] = InvoiceForm(initial=model_to_dict(instance))

    if instance:
        context["formset"] = django_json_dumps(list(instance.invoiceitem_set.values()))

    return render(request, template_name="invoices/invoice.html",
                  context=context)


@login_required
def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    context = {"object": invoice}

    if request.method == "POST":
        return redirect("list")

    return render(request, template_name="invoices/confirm_delete.html",
                  context=context)


@login_required
def list_invoices(request):
    queryset = Invoice.objects.filter(company=request.company)
    pager = Paginator(queryset, 15)
    page = pager.page(request.GET.get("page", 1))

    return render(request, template_name='invoices/invoice_list.html',
                  context={"objects": page.object_list, "pager": pager, "page": page})


# @login_required
# def preview(request, pk, base_template="print.html"):
#     return _invoice(request, pk, base_template=base_template,
#                    print=True)


# @login_required
# def print(request, pk):
#     import os
#     from xhtml2pdf import pisa
#     from io import BytesIO
#
#     css = [
#         os.path.dirname(__file__) + static("invoices/custom/bootstrap.united.min.css"),
#         os.path.dirname(__file__) + static("invoices/custom/app.css"),
#     ]
#
#     styles = [open(css_file).read() for css_file in css]
#     context = {"styles": styles}
#     response = _invoice(request, pk, base_template="print.html", print=True, context=context)
#     result = BytesIO()
#
#     pdf = pisa.pisaDocument(response.getvalue(), result, encoding="utf-8")
#     if not pdf.err:
#         response = HttpResponse(result.getvalue(), content_type="application/pdf")
#         # response["Content-Disposition"] = "attachment; filename='invoice.pdf'"
#         return response
#     return HttpResponse('We had some errors printing the document!')
