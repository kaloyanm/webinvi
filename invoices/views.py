# -*- coding: utf-8 -*-

import json
import urllib.request
import logging
import urllib

from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404

from core.forms import CompanyForm
from core.models import Company
from invoices.forms import InvoiceForm, InvoiceItemFormSet, SearchForm
from invoices.models import Invoice, InvoiceItem, get_next_number

from prices import Price
from django_prices_openexchangerates import exchange_currency
from invoices.tasks import save_invoice_to_google_drive
from invoices.util import get_pdf_generator_url

logger = logging.getLogger(__name__)


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


def sync_invoice_to_external(instance, user):
    # Store in Google Drive Here
    if user.settings.gdrive_sync:
        sync_settings = {
            'gdrive_sync': user.settings.gdrive_sync,
            'invoice_id': instance.id,
            'filename': "{}-{}-{}.pdf".format(
                instance.company.name,
                instance.invoice_type,
                instance.number
            ),
        }
        save_invoice_to_google_drive.delay(user.id, sync_settings)


def _invoice(request, pk=None, invoice_type="invoice",
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
        "released_at": str(timezone.now().strftime("%Y-%m-%d")),
        "taxevent_at": str(timezone.now().strftime("%Y-%m-%d")),
    }

    context = {
        "print": print,
        "base_template": base_template,
        "form": InvoiceForm(initial=default_data),
        "instance": instance,
        "formset": json.dumps([]),
        "invoice_type": invoice_type,
        "company_form": CompanyForm(instance=company),
        "pk": pk,
    }

    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=instance)
        form_items = InvoiceItemFormSet(request.POST)

        if process_invoice(request, form, form_items):

            sync_invoice_to_external(instance, request.user)
            return redirect(reverse(invoice_type, args=[pk]))

        context["form"] = form
    else:
        if instance:
            context["company_form"] = CompanyForm(instance=instance.company)
            context["form"] = InvoiceForm(instance=instance)

    if instance:
        context["formset"] = django_json_dumps(list(instance.invoiceitem_set.values()))

    rates = {}
    for from_c in settings.ALLOWED_CURRENCIES:
        rates[from_c] = round(exchange_currency(Price(1, currency=from_c), 'BGN').net, 5)
    context['rates'] = rates
    context['rates_json'] = django_json_dumps(rates)

    return render(request, template_name="invoices/invoice.html",
                  context=context)


@login_required
def invoice(*args, **kwargs):
    return _invoice(*args, **kwargs)


@login_required
def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.delete()
    return redirect("list")


def search_invoices(company, search_terms):
    from django.contrib.postgres.search import SearchQuery, SearchVector
    queryset = Invoice.objects.filter(company=company)

    def terms2query(search_terms):
        terms = search_terms.split(" ")
        out = SearchQuery(terms.pop())
        for term in terms:
            out = out | SearchQuery(term)
        return out

    if search_terms:
        search_vector_fields = ['client_name', 'client_city',
                                'client_mol', 'client_address']
        queryset = queryset.annotate(search=SearchVector(*search_vector_fields))\
            .filter(search=terms2query(search_terms))
    return queryset


@login_required
def list_invoices(request, company_pk=None):
    company_pk = company_pk if company_pk else request.session.get('company_pk')
    if company_pk:
        try:
            company = Company.objects.get(pk=company_pk)
            request.session['company_pk'] = company_pk
        except Company.DoesNotExist:
            raise Http404
    else:
        company = request.company

    search_terms = request.GET.get("query", "")
    queryset = search_invoices(company, search_terms)

    pager = Paginator(queryset, 15)
    page = pager.page(request.GET.get("page", 1))

    context = {
        "objects": page.object_list,
        "pager": pager,
        "page": page,
        "query": search_terms,
        "company": company,
        "companies": request.user.company_set.all().values_list('id', 'name', 'eik'),
    }

    return render(request, template_name='invoices/invoice_list.html',
                  context=context)


def print_preview(request, token):
    try:
        invoice_pk = cache.get(token)
        invoice = Invoice.objects.get(pk=invoice_pk)
        request.user = invoice.company.user
        request.company = invoice.company
    except Invoice.DoesNotExist:
        raise Http404

    return _invoice(request, pk=invoice_pk, base_template="print.html",
                    print=True)


@login_required
def print_invoice(request, pk):
    pdf_generator_url = get_pdf_generator_url(pk)

    req = urllib.request.Request(pdf_generator_url)
    with urllib.request.urlopen(req) as res:
        if res.status == 200:
            response = HttpResponse(res.read(), content_type="application/pdf")
            # response["Content-Disposition"] = "attachment; filename='invoice.pdf'"
            return response
        else:
            raise Http404
