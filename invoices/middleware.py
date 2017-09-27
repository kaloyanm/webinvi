
from core.models import Company


class UserCompanyMiddleware(object):

    def process_request(self, request):
        if request.user and not request.user.is_anonymous():
            company_pk = request.session.get('company_pk')
            if company_pk:
                clause = dict(user=request.user, pk=company_pk)
            else:
                clause = dict(user=request.user, default=True)

            try:
                request.company = Company.objects.get(**clause)
            except Company.DoesNotExist:
                request.company = None
