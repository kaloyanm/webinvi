from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       UserCreationForm)
from django.core.urlresolvers import reverse_lazy
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic

from core.models import Company
from core.forms import CompanyForm
from invoices.models import Invoice

import logging
logger = logging.getLogger(__name__)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('home'))


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
        
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.cleaned_data["user"] = request.user
            obj, created = Company.objects.update_or_create(pk=pk, defaults=form.cleaned_data)
            # if created:
            #     obj.user = request.user
            #     obj.save()
            return redirect("companies")
    else:
        form = CompanyForm(initial=data)

    return render(request, template_name="core/company.html",
                  context={"form": form, "pk": pk})

@login_required
def drop_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    company.delete()
    return redirect("companies")
