from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, update_session_auth_hash
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.db.models import Q
from django.forms.models import model_to_dict

from core.models import Company
from core.forms import (
    LoginForm,
    ChangePassForm,
    RegistratiоnForm,
    CompanyForm,
    CompaniesImportForm,
    InvoiceproImportForm,
)

from hvad.utils import get_translation
from core.admin import CompanyResource
from core.import_export.invoicepro import read_invoicepro_file


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('home'))


def contact(request):
    return render(request, 'contact.html')


def home(request):
    return render(request, 'home.html')


class LoginView(generic.FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


@login_required
def change_password(request):
    form = ChangePassForm(request.user)

    if request.method == "POST":
        form = ChangePassForm(request.user, request.POST)
        if form.is_valid():
            form.save(commit=True)
            update_session_auth_hash(request, form.user)
            return redirect(reverse_lazy("password"))

    context = {"form": form}
    return render(request, template_name="change_password.html", context=context)


class RegistrationView(generic.FormView):
    form_class = RegistratiоnForm
    template_name = '_registration.html'


@login_required
def companies(request):
    clauses = Q(user=request.user) or Q(companyaccess__user=request.user, companyaccess__verified=True)
    objects = Company.objects.filter(clauses)
    context = {"objects": objects}
    return render(request, template_name="core/_companies.html", context=context)


@login_required
def company(request, pk=None, language_code=settings.LANGUAGE_CODE):
    if pk:
        try:
            instance = Company.objects.language(language_code).get(pk=pk, user=request.user)
        except Company.DoesNotExist:
            raise Http404
    else:
        instance = None
    form = CompanyForm(instance=instance)

    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect("companies")

    return render(request, template_name="core/_company.html",
                  context={"form": form, "pk": pk})


@login_required
def drop_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    company.delete()
    return redirect("companies")


@login_required
def export_companies(request):
    queryset = Company.objects.filter(user=request.user)
    dataset = CompanyResource().export(queryset=queryset)

    response = HttpResponse(dataset.csv, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename=companies.csv'
    return response


class ImportException(Exception):
    pass


def get_import_errors(result):
    all_errors = []
    output = []
    for (index, errors) in result.row_errors():
        [all_errors.append(suberror) for suberror in errors]

    for err in all_errors:
        output.append({
            "error": err.error,
            "traceback": err.traceback,
            "row": err.row
        })
    return output


def import_csv_upload(resource_instance, file_in_memory):
    import tablib

    file_in_memory.open() # just in case reset the file pointer
    headers = next(file_in_memory.file).decode("utf-8").strip().split(",")
    headers = tuple(headers)

    if headers != resource_instance._meta.fields:
        raise ImportException("Mismatch header")

    content = []
    while True:
        try:
            line = next(file_in_memory.file)
        except StopIteration:
            break
        line = line.decode("utf-8").strip().split(",")
        content.append(tuple(line))

    dataset = tablib.Dataset()
    dataset.headers = headers
    dataset.extend(content)

    result = resource_instance.import_data(dataset, dry_run=False)
    if result.has_errors():
        raise ImportException()

    return True


@login_required
def import_companies(request):
    form = CompaniesImportForm()

    if request.method == "POST":
        form = CompaniesImportForm(request.POST, request.FILES)

        if form.is_valid():
            company_resource = CompanyResource(user=request.user)
            try:
                import_csv_upload(company_resource, request.FILES["file"])
                return redirect(reverse_lazy("companies"))
            except ImportException as e:
                raise Http404

    return render(request, template_name="core/_import_companies.html",
                  context={"form": form})


@login_required
def import_invoicepro(request):
    form = InvoiceproImportForm()

    if request.method == "POST":
        form = InvoiceproImportForm(request.POST, request.FILES)

        if form.is_valid():
            company_resource = CompanyResource(user=request.user)
            try:
                invoicepro_file = read_invoicepro_file(request.FILES["file"])
                companies_dataset = invoicepro_file['companies'].as_dataset({
                    'id': 'id',
                    'Name_bg': 'name',
                    'Bulstat': 'eik',
                    'VatId': 'dds',
                    'Address_bg': 'address',
                    'City_bg': 'city',
                    'Mol_bg': 'mol',
                })
                result = company_resource.import_data(companies_dataset, dry_run=False)
                if result.has_errors():
                    raise ImportException()

                return redirect(reverse_lazy("companies"))
            except ImportException as e:
                raise Http404

    return render(request, template_name="core/_import_invoicepro.html",
                  context={"form": form})


def test_semantic(request):
    context = {'form': ExampleSemanticForm}
    return render(request, 'test/_semantic.html', context)
