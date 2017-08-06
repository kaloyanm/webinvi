
import factory
import random
from django.auth.models import User
from core.models import Company


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name_female')
    last_name = factory.Faker('last_name_female')
    email = factory.Faker('email')
    is_active = True
    is_staff = True
    is_admin = False


class CompanyFactory(factory.DjangoModelFactory):
    class Meta:
        model = Company

    user = UserFactory.create()
    name = factory.Faker('company', locale='bg_BG')
    city = factory.Faker('city')
    address = factory.Faker('address')
    mol = factory.Faker('name')
    eik = random.randint(1234567891, 2345678912) # any ten digits number would suffice
