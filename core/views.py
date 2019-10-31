import logging
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, update_session_auth_hash, authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.conf import settings

from django.template import Context
from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template
from django_mailgun import MailgunAPIError

from password_reset.forms import PasswordResetForm, PasswordRecoveryForm
from password_reset.views import Recover, RecoverDone, Reset, ResetDone

from core.mixins import SemanticUIFormMixin
from core.models import Company
from core.forms import (
    LoginForm,
    ChangePassForm,
    RegistrationForm,
    CompanyForm,
    ContactForm,
)
from core.admin import CompanyResource

logger = logging.Logger(__name__)


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('home'))


def contact(request):
    form_class = ContactForm
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']

            template = get_template('contact_template.txt')
            context = Context({
                'name': name,
                'email': email,
                'phone': phone,
                'message': message,
            })

            content = template.render(context)

            email_message = EmailMessage(
                'Email from WebInvoices',
                content,
                'support@webinvoices.eu',
                ['kaloyan.mir4ev@gmail.com'],
                headers={'Reply-To': email}
            )
            email_message.send()
            return redirect('thanks')

    context = {"form": form_class}
    return render(request, 'contact.html', context)


def home(request):
    if request.user:
        return redirect('list_invoices')
    else:
        return redirect('login')
    #  return render(request, 'home.html')  # leave the front page for better times


def thanks(request):
    return render(request, 'thanks.html')


class LoginView(generic.FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('list_invoices')

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


def registration(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            User = get_user_model()
            user, created = User.objects.get_or_create(username=form.cleaned_data['username'])
            if created:
                user.set_password(form.clean_password2())
                user.save()
                try:
                    send_mail(_("{}: Нов потребител").format(settings.HOSTNAME), [_("Регистрация")],
                              settings.NO_REPLY_EMAIL, [user.username])
                except MailgunAPIError as e:
                    logger.error("mailgun error", e, e.args[0].text)

                user = authenticate(username=user.username, password=form.clean_password2())
                login(request, user)
                return redirect(reverse_lazy('list_invoices'))
    return render(request, template_name='_registration.html', context={"form": form})


@login_required
def companies(request):
    objects = Company.objects.filter(user=request.user)
    return render(request, template_name="core/_companies.html", context={"objects": objects})


@login_required
def company(request):
    if request.method == "POST":
        form = CompanyForm(request.POST, instance=request.user.settings)
        if form.is_valid():
            form.save()
            return redirect("company")
    else:
        form = CompanyForm(instance=request.user.settings)

    return render(request, template_name="core/_company.html",
                  context={"form": form})


@login_required
def drop_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if company.has_invoices:
        messages.warning(request, _("Моля първо си изтрийте фактурите към тази фирма!"))
        return redirect(reverse('company', args=[pk]))

    company.delete()
    return redirect("companies")


@login_required
def export_companies(request):
    queryset = Company.objects.filter(user=request.user)
    dataset = CompanyResource().export(queryset=queryset)

    response = HttpResponse(dataset.csv, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename=companies.csv'
    return response


class AppPasswordResetForm(SemanticUIFormMixin, PasswordResetForm):
    submit_button_label = _("Смени")


class ResetView(Reset):
    form_class = AppPasswordResetForm
    template_name = "_password_recover.html"


class AppPasswordRecoveryForm(SemanticUIFormMixin, PasswordRecoveryForm):
    submit_button_label = _("Възстанови")

    def __init__(self, *args, **kwars):
        super().__init__(*args, **kwars)
        self.fields['username_or_email'].label = _("Email")


class RecoverView(Recover):
    form_class = AppPasswordRecoveryForm
    template_name = "_password_recover.html"
    search_fields = ['username']

    def form_valid(self, form):
        form.cleaned_data['user'].email = form.cleaned_data['user'].username  # hacky
        return super().form_valid(form)


class RecoverDoneView(RecoverDone):
    template_name = "_password_sent.html"


class ResetDoneView(ResetDone):
    template_name = "_password_reset_done.html"
