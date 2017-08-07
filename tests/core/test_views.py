
import pytest
from core.views import company
from core.test.factories import CompanyFactory, UserFactory


@pytest.mark.django_db
def test_company_view(rf):
    user = UserFactory.create()
    _company = CompanyFactory(user=user)

    request = rf.get('')
    request.user = user
    response = company(request, _company.pk)

    assert response.status_code == 200
    assert response.template_name == "core/_company.html"