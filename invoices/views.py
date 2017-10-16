# -*- coding: utf-8 -*-

import json
import urllib.request
import logging
import urllib

from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404, JsonResponse

from core.forms import CompanyForm
from core.models import Company
from invoices.forms import InvoiceForm, InvoiceItemFormSet
from invoices.models import Invoice, InvoiceItem, get_next_number

from prices import Price
from django_prices_openexchangerates import exchange_currency
from invoices.tasks import save_invoice_to_google_drive
from invoices.util import get_pdf_generator_url

logger = logging.getLogger(__name__)


def django_json_dumps(items):
    return json.dumps(items, cls=DjangoJSONEncoder)


def get_company_or_404(request, company_pk=None):
    company_pk = company_pk if company_pk else request.session.get('company_pk')
    if company_pk:
        try:
            company = Company.objects.get(pk=company_pk, user=request.user)
            request.session['company_pk'] = company_pk
        except Company.DoesNotExist:
            raise Http404
    else:
        company = request.company
    return company


def process_invoice(form, form_items):
    pk = None
    if form.is_valid() and form_items.is_valid():
        instance = form.save()

        with transaction.atomic():
            existing_pks = []
            for form in form_items:
                item_pk = form.cleaned_data['id']
                del form.cleaned_data['id']
                del form.cleaned_data['DELETE']

                form.cleaned_data['invoice'] = instance
                obj, created = InvoiceItem.objects.update_or_create(pk=item_pk, defaults=form.cleaned_data)
                existing_pks.append(obj.pk)

            deleted_pks = set(instance.invoiceitem_set.all().values_list('pk', flat=True)).difference(set(existing_pks))
            instance.invoiceitem_set.filter(pk__in=deleted_pks).delete()

        return True, instance.pk
    return False, pk


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
        invoice_type = instance.invoice_type
        company = instance.company
    else:
        instance = None
        company = get_company_or_404(request)

    if not company:
        return redirect(reverse("company"))

    default_data = {
        "number": get_next_number(request.company, invoice_type),
        "released_at": str(timezone.now().strftime("%Y-%m-%d")),
        "taxevent_at": str(timezone.now().strftime("%Y-%m-%d")),
    }

    if pk:
        selected_language = request.session.get('current_lang', settings.LANGUAGE_CODE)
    else:
        selected_language = settings.LANGUAGE_CODE
        request.session['current_lang'] = settings.LANGUAGE_CODE  # restore the default lang in case of editing recorded translation

    context = {
        "print": print,
        "base_template": base_template,
        "form": InvoiceForm(initial=default_data),
        "instance": instance,
        "items": json.dumps([]),
        "invoice_type": invoice_type,
        "company_form": CompanyForm(instance=company),
        "pk": pk,
        "selected_language": selected_language,
        "use_tr": pk and selected_language != settings.LANGUAGE_CODE,
    }

    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=instance)
        initial_items = list(instance.invoiceitem_set.all().values()) if instance else []
        form_items = InvoiceItemFormSet(request.POST, initial=initial_items)

        is_ok, pk = process_invoice(form, form_items)
        if is_ok:
            sync_invoice_to_external(instance, request.user)
            return redirect(reverse(invoice_type, args=[pk]))

        context["form_items"] = form_items
        context["form"] = form
    elif instance:
        context["company_form"] = CompanyForm(instance=instance.company)
        context["form"] = InvoiceForm(instance=instance)

    if instance:
        context["items"] = django_json_dumps(list(instance.invoiceitem_set.values()))

    rates = {}
    for from_c in settings.ALLOWED_CURRENCIES:
        rates[from_c] = round(exchange_currency(Price(1.0000, currency=from_c), 'BGN').net, 5)
    if instance and instance.currency:
        rates[instance.currency] = instance.currency_rate

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


def search_invoices_queryset(company, search_terms):
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


def get_company_or_404(request, company_pk=None):
    company_pk = company_pk if company_pk else request.session.get('company_pk')
    if company_pk:
        try:
            company = Company.objects.get(pk=company_pk)
            request.session['company_pk'] = company_pk
        except Company.DoesNotExist:
            raise Http404
    else:
        company = request.company
    return company


@login_required
def list_invoices(request, company_pk=None):
    company = get_company_or_404(request, company_pk)
    search_terms = request.GET.get("query", "")
    queryset = search_invoices_queryset(company, search_terms)

    pager = Paginator(queryset, settings.INVOICES_PER_PAGE)
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
    instance = get_object_or_404(Invoice, pk=pk)

    req = urllib.request.Request(pdf_generator_url)
    with urllib.request.urlopen(req) as res:
        if res.status == 200:
            response = HttpResponse(res.read(), content_type="application/pdf")
            return response
        else:
            raise Http404


def get_searchfield_queryset(company, field_name, keyword):
    try:
        queryset = Invoice.objects.filter(company=company)
        kwargs = {
            "{}__{}".format(field_name, "gt"): '',
        }
        if keyword:
            kwargs["{}__{}".format(field_name, "icontains")] = keyword
        return queryset.filter(**kwargs).order_by(field_name).distinct(field_name)
    except Exception:
        raise Http404


@login_required
def autocomplete_field(request):
    company = get_company_or_404(request, company_pk=None)
    field_name = request.GET.get('f')
    keyword = request.GET.get('k')

    queryset = get_searchfield_queryset(company, field_name, keyword)
    data = queryset.values_list(field_name, flat=True)[:10]

    response = {"results": [{"title": item} for item in data]}
    return JsonResponse(response)


@login_required
def autocomplete_client(request):
    company = get_company_or_404(request, company_pk=None)
    keyword = request.GET.get('k')

    selected_language = request.session.get('current_lang', settings.LANGUAGE_CODE)
    use_tr = selected_language != settings.LANGUAGE_CODE

    fields = ['client_city', 'client_address', 'client_mol', 'client_name']
    if use_tr:
        fields = ["{}_tr".format(field) for field in fields]
    fields += ['client_eik', 'client_dds']

    queryset = get_searchfield_queryset(company, 'client_name', keyword)
    raw_data = queryset.values(*fields)

    data = []
    for entry in raw_data[:10]:
        entry["title"] = entry["client_name"]
        data.append(entry)

    response = {"results": data}
    return JsonResponse(response)


@login_required
def change_invoice_language(request, pk, lang):
    allowed_langs = [code for code, _ in settings.LANGUAGES]
    if lang in allowed_langs:
        request.session['current_lang'] = lang
    return redirect(reverse('invoice', args=[pk]))


@login_required
def proforma2invoice(request, pk):
    company = get_company_or_404(request)
    instance = get_object_or_404(Invoice, pk=pk, invoice_type=Invoice.INVOICE_TYPE_PROFORMA,
                                 company=company)
    items = instance.invoiceitem_set.all()

    instance.pk = None
    instance.number = None
    instance.invoice_type = Invoice.INVOICE_TYPE_INVOICE
    instance.released_at = timezone.now().strftime("%Y-%m-%d")
    instance.save()

    with transaction.atomic():
        for item in items:
            item.pk = None
            item.invoice = instance
            item.save()
        messages.success(request, _("The invoice has been created successfully."))
    return redirect(reverse('invoice', args=[instance.pk]))
