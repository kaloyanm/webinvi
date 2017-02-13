from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy


class AppLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')