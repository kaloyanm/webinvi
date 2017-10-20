
from core.models import Company


class UserCompanyMiddleware(object):

    def process_request(self, request):
        if request.user and not request.user.is_anonymous():
            clause = dict(user=request.user)
            company_pk = request.session.get('company_pk')

            if company_pk:
                clause['pk'] = company_pk

            try:
                request.company = Company.objects.filter(**clause).first()
            except Company.DoesNotExist:
                request.company = None
