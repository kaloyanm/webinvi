from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       UserCreationForm)
from django.core.urlresolvers import reverse_lazy
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic

from core.forms import CompanySettingsForm


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


class CompanySettingsView(generic.FormView):
    form_class = CompanySettingsForm
    template_name = 'profile.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        return model_to_dict(self.request.user.profile)
