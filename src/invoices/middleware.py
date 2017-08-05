
from django.shortcuts import redirect
from core.models import Company


class UserCompanyMiddleware:

    def process_request(self, request):
        if request.user and not request.user.is_anonymous():
            try:
                request.company = Company.objects.get(user=request.user, default=True)
            except Company.DoesNotExist:
                request.company = None
