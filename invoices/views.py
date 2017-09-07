# -*- coding: utf-8 -*-

import json
import os

from xhtml2pdf import pisa
from io import StringIO, BytesIO
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404

from core.forms import CompanyForm
from invoices.forms import InvoiceForm, InvoiceItemFormSet, SearchForm
from invoices.models import Invoice, InvoiceItem, get_next_number


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
def invoice(request, pk=None, invoice_type="invoice",
            base_template="base.html", print=None):
    if pk:
        instance = get_object_or_404(Invoice, pk=pk)
        company = instance.company
    else:
        instance = None
        company = request.company

    if not company:
        return redirect(reverse("company"))

    default_data = {
        "number": get_next_number(request.company, invoice_type),
        "released_at": str(timezone.now()),
        "taxevent_at": str(timezone.now()),
    }

    context = {
        "print": print,
        "base_template": base_template,
        "form": InvoiceForm(initial=default_data),
        "formset": json.dumps([]),
        "invoice_type": invoice_type,
        "company_form": CompanyForm(model_to_dict(company)),
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
    context = {"object": get_object_or_404(Invoice, pk=pk)}

    if request.method == "POST":
        return redirect("list")

    return render(request, template_name="invoices/confirm_delete.html",
                  context=context)


@login_required
def list_invoices(request):
    queryset = Invoice.objects.filter(company=request.company)

    search_q = request.GET.get("query", "")
    if search_q:
        form = SearchForm({"terms": search_q})
        if form.is_valid():
            terms = form.cleaned_data.get("terms")
            queryset = queryset.filter(client_name__icontains=terms)

    pager = Paginator(queryset, 15)
    page = pager.page(request.GET.get("page", 1))

    context = {
        "objects": page.object_list,
        "pager": pager,
        "page": page,
        "query": search_q,
    }

    return render(request, template_name='invoices/invoice_list.html',
                  context=context)


@login_required
def preview(request, pk, base_template="print.html"):
    return invoice(request, pk, base_template=base_template,
                   print=True)

@login_required
def webprint(request, pk):
    def fetch_resources(uri, rel):
        if uri.startswith("http"):
            path = uri
        else:
            path = os.path.join(settings.STATIC_ROOT, uri.replace(settings.STATIC_URL, ""))
        return path

    response = preview(request, pk)
    return response
    result = BytesIO()
    pdf = pisa.pisaDocument(response.content, dest=result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename='invoice.pdf'"
        return response
    else:
        raise Http404
