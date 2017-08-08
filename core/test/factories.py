
import factory
import random
from django.contrib.auth import get_user_model
from core.models import Company

User = get_user_model()

class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', )

    username = factory.Sequence(lambda n: 'user%d' % n)
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')
    first_name = factory.Faker('first_name_female')
    last_name = factory.Faker('last_name_female')
    email = factory.Faker('email')
    is_active = True
    is_staff = False
    is_superuser = False


class CompanyFactory(factory.DjangoModelFactory):
    class Meta:
        model = Company

    user = factory.SubFactory('core.test.factories.UserFactory')
    name = factory.Faker('company', locale='bg_BG')
    city = factory.Faker('city', locale='bg_BG')
    address = factory.Faker('address', locale='bg_BG')
    mol = factory.Faker('name', locale='bg_BG')
    eik = factory.Sequence(lambda n: 2345678912 - n) # any ten digits number would suffice
