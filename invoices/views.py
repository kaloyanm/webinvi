import json
import urllib.request
import logging
import urllib

from django import forms
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
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse, Http404, JsonResponse

from core.forms import CompanyForm
from core.models import Company
from core.utils import get_translation_in
from invoices.forms import InvoiceForm, InvoiceItemFormSet
from invoices.models import Invoice, InvoiceItem, get_next_number

from prices import Price
from django_prices_openexchangerates import exchange_currency
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
            company = request.company
    else:
        company = request.company

    if not company:
        raise Http404
    return company


def process_invoice(form, form_items):
    pk = None
    if form.is_valid() and form_items.is_valid():
        instance = form.save()
        existing_pks = []

        with transaction.atomic():
            for form in form_items:
                item_pk = form.cleaned_data['id']
                del form.cleaned_data['DELETE']
                del form.cleaned_data['id']
                form.cleaned_data['invoice'] = instance

                if item_pk:
                    InvoiceItem.objects.filter(pk=item_pk).update(**form.cleaned_data)
                    existing_pks.append(item_pk)
                else:
                    obj = InvoiceItem(**form.cleaned_data)
                    obj.save()
                    existing_pks.append(obj.pk)

            deleted_pks = set(instance.invoiceitem_set.all().values_list('pk', flat=True)).difference(set(existing_pks))
            instance.invoiceitem_set.filter(pk__in=deleted_pks).delete()

        return True, instance.pk
    return False, pk


def _invoice(request, pk=None, invoice_type="invoice",
             base_template="base.html", to_print=None, lang_code=None):
    if pk:
        instance = get_object_or_404(Invoice, pk=pk)
        invoice_type = instance.invoice_type
    else:
        instance = None

    default_data = {
        "number": get_next_number(request.user, invoice_type),
        "released_at": str(timezone.now().strftime("%Y-%m-%d")),
        "taxevent_at": str(timezone.now().strftime("%Y-%m-%d")),
    }

    if pk:
        selected_language = request.session.get('current_lang', lang_code)
        selected_language = selected_language if selected_language else settings.LANGUAGE_CODE
    else:
        selected_language = settings.LANGUAGE_CODE
        request.session['current_lang'] = settings.LANGUAGE_CODE  # restore the default lang in case of editing recorded translation

    context = {
        "print": to_print,
        "base_template": base_template,
        "form": InvoiceForm(initial=default_data),
        "instance": instance,
        "items": json.dumps([]),
        "invoice_type": invoice_type,
        "company_form": CompanyForm(instance=request.user.settings),
        "pk": pk,
        "selected_language": selected_language,
    }

    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=instance)
        initial_items = list(instance.invoiceitem_set.all().values()) if instance else []
        form_items = InvoiceItemFormSet(request.POST, initial=initial_items)

        is_ok, pk = process_invoice(form, form_items)
        if is_ok:
            return redirect(reverse(invoice_type, args=[pk]))

        context["form_items"] = form_items
        context["form"] = form
    elif instance:
        context["company_form"] = CompanyForm(instance=instance.user.settings)
        context["form"] = InvoiceForm(instance=instance)

    if not pk and request.user.settings.payment_iban:
        context["form"]["payment_type"].value = context["company_form"]["payment_type"].value
        context["form"]["payment_iban"].value = context["company_form"]["payment_iban"].value
        context["form"]["payment_swift"].value = context["company_form"]["payment_swift"].value
        context["form"]["payment_bank"].value = context["company_form"]["payment_bank"].value

    if instance:
        context["items"] = django_json_dumps(list(instance.invoiceitem_set.values()))

    # rates = {}
    # for from_c in settings.ALLOWED_CURRENCIES:
    #     rates[from_c] = round(exchange_currency(Price(1.0000, currency=from_c), 'BGN').net, 5)
    # if instance and instance.currency:
    #     rates[instance.currency] = instance.currency_rate

    # context['rates'] = rates
    # context['rates_json'] = django_json_dumps(rates)

    return render(request, template_name="invoices/_invoice.html",
                  context=context)


@login_required
def invoice_details(*args, **kwargs):
    return _invoice(*args, **kwargs)


@login_required
def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk, deleted=False)
    invoice.deleted = True
    invoice.save()
    return redirect("list")


def search_invoices_queryset(user, search_terms, invoice_type=None):
    from django.contrib.postgres.search import SearchQuery
    from django.db.models import Q

    queryset = Invoice.objects.filter(user=user)
    if invoice_type:
        queryset = queryset.filter(invoice_type=invoice_type)

    if search_terms:
        query = SearchQuery(search_terms)
        conditions = Q(search_vector=query)
        try:
            conditions = conditions | Q(number=int(search_terms))
        except ValueError:
            pass
        queryset = queryset.filter(conditions)
    return queryset


def get_company_or_404(request, company_pk=None):
    company_pk = company_pk if company_pk else request.session.get('company_pk')
    if company_pk:
        try:
            company = Company.objects.get(pk=company_pk, user=request.user)
            request.session['company_pk'] = company_pk
        except Company.DoesNotExist:
            company = request.company
    else:
        company = request.company

    if not company:
        raise Http404
    return company


@login_required
def list_invoices(request, company_pk=None):
    class SearchForm(forms.Form):
        query = forms.CharField(max_length=200, required=False)
        t = forms.CharField(max_length=55, required=False)
        page = forms.IntegerField(required=False)

    search_form = SearchForm(request.GET, initial={"page": 1})
    search_form.is_valid()
    search_terms = search_form.cleaned_data.get("query", "")
    selected_type = search_form.cleaned_data.get("t", "")

    queryset = search_invoices_queryset(request.user, search_terms, invoice_type=selected_type)
    invoice_types = list(Invoice.INVOICE_TYPES)
    invoice_types.insert(0, ('', _('Всички')))

    pager = Paginator(queryset, settings.INVOICES_PER_PAGE)
    try:
        page = pager.page(search_form.cleaned_data.get("page") or 1)
    except EmptyPage:
        page = pager.page(1)

    context = {
        "objects": page.object_list,
        "pager": pager,
        "page": page,
        "query": search_terms,
        "company": request.user.settings,
        "invoice_types": invoice_types,
        "selected_type": selected_type,
        "companies": [],
    }

    return render(request, template_name='invoices/invoice_list.html',
                  context=context)


def print_preview(request, token, lang_code):
    try:
        invoice_pk = cache.get(token)
        invoice = Invoice.objects.get(pk=invoice_pk)
        request.user = invoice.user
    except Invoice.DoesNotExist:
        raise Http404

    return _invoice(request, pk=invoice_pk, base_template="print.html",
                    to_print=True, lang_code=lang_code)


@login_required
def print_invoice(request, pk):
    lang_code = request.session.get('current_lang', settings.LANGUAGE_CODE)
    pdf_generator_url = get_pdf_generator_url(pk, lang_code)
    get_object_or_404(Invoice, pk=pk)

    req = urllib.request.Request(pdf_generator_url)
    with urllib.request.urlopen(req) as res:
        if res.status == 200:
            response = HttpResponse(res.read(), content_type="application/pdf")
            return response
        else:
            raise Http404


def get_searchfield_queryset(user, field_name, keyword):
    try:
        kwargs = {
            "{}__{}".format(field_name, "gt"): '',
            "user": user,
        }
        if keyword:
            kwargs["{}__{}".format(field_name, "icontains")] = keyword

        return Invoice.objects.filter(**kwargs).order_by(field_name).distinct(field_name)
    except Exception:
        raise Http404


@login_required
def autocomplete_field(request):
    from core.business_settings import PAYMENT_TYPES, NO_DDS_REASONS

    default_values = {
        "payment_type": (PAYMENT_TYPES, 'bg'),
        "no_dds_reason": (NO_DDS_REASONS, 'bg'),
    }

    field_name = request.GET.get('f')
    keyword = request.GET.get('k')

    queryset = get_searchfield_queryset(request.user, field_name, keyword)
    data = queryset.values_list(field_name, flat=True)[:10]

    if field_name in default_values:
        choices, locale = default_values.get(field_name)
        if keyword:
            choices = filter(lambda s: s.find(keyword)!=-1, choices)
        result = [{"title": get_translation_in(item, locale)} for item in choices]
    else:
        result = [{"title": item} for item in data]

    response = {"results": result}
    return JsonResponse(response)


@login_required
def autocomplete_client(request):
    keyword = request.GET.get('k')
    fields = ['client_city', 'client_address', 'client_mol', 'client_name', 'client_eik', 'client_dds']
    queryset = get_searchfield_queryset(request.user, 'client_name', keyword)
    raw_data = queryset.values(*fields)

    data = []
    for entry in raw_data[:10]:
        entry["title"] = entry['client_name']
        data.append(entry)

    response = {"results": data}
    return JsonResponse(response)


@login_required
def change_invoice_language(request, pk, lang):
    allowed_langs = [code for code, _ in settings.LANGUAGES]
    if lang in allowed_langs:
        request.session['current_lang'] = lang
    return redirect(reverse('invoice', args=[pk]))


def copy_invoice(instance, invoice_type, save_ref=False):
    items = instance.invoiceitem_set.all()
    ref_number = instance.number

    instance.pk = None
    instance.number = None
    instance.ref_number = ref_number if save_ref else None
    instance.invoice_type = invoice_type
    instance.released_at = timezone.now().strftime("%Y-%m-%d")
    instance.save()

    with transaction.atomic():
        for item in items:
            item.pk = None
            item.invoice = instance
            item.save()
    return instance.pk


@login_required
def proforma2invoice(request, pk):
    instance = get_object_or_404(Invoice, pk=pk, invoice_type=Invoice.INVOICE_TYPE_PROFORMA)
    new_pk = copy_invoice(instance, Invoice.INVOICE_TYPE_INVOICE)
    if new_pk:
        messages.success(request, _("Фактурата беше създадена успешно."))
    return redirect(reverse('invoice', args=[instance.pk]))


@login_required
def invoice2announce(request, pk, announce_type):
    if announce_type not in [Invoice.INVOICE_TYPE_CREDIT, Invoice.INVOICE_TYPE_DEBIT]:
        raise Http404

    instance = get_object_or_404(Invoice, pk=pk, user=request.user,
                                 invoice_type=Invoice.INVOICE_TYPE_INVOICE)

    new_pk = copy_invoice(instance, announce_type, save_ref=True)
    return redirect(reverse(announce_type, args=[new_pk]))
