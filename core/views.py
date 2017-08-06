
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       UserCreationForm)
from django.core.urlresolvers import reverse_lazy
from django.forms.models import model_to_dict
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic

from core.models import Company
from core.forms import CompanyForm, CompaniesImportForm
from core.admin import CompanyResource


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('home'))


def contact(request):
    return render(request, 'contact.html')


def home(request):
    return render(request, 'home.html')


class LoginView(generic.FormView):
    form_class = AuthenticationForm
    template_name = 'login.html'
    success_url = reverse_lazy('list')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class PasswordChangeView(generic.FormView):
    form_class = PasswordChangeForm
    template_name = 'change_password.html'

    def get_initial(self):
        self.initial = {}
        return super().get_initial()

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['data'] = self.request.POST
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save(commit=True)
        update_session_auth_hash(self.request, form.user)
        return super(PasswordChangeView, self).form_valid(form)


class RegistrationView(generic.FormView):
    form_class = UserCreationForm
    template_name = '_registration.html'


@login_required
def companies(request):
    objects = Company.objects.filter(user=request.user)
    context = {"objects": objects}
    return render(request, template_name="core/companies.html",
                  context=context)


@login_required
def company(request, pk=None):
    if pk:
        company = get_object_or_404(Company, pk=pk)
        data = model_to_dict(company)
    else:
        data = None
    form = CompanyForm(initial=data)

    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.cleaned_data["user"] = request.user
            Company.objects.update_or_create(pk=pk, defaults=form.cleaned_data)
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
    print(get_import_errors(result))
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

    context = { "form": form}
    return render(request, template_name="core/_import_companies.html", context=context)

