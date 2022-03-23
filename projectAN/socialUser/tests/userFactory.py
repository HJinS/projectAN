from rest_framework.test import APIClient, APITestCase
import factory, pytz, uuid
from ..models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        exclude = ('username')
        
    id = factory.sequence(lambda n: n+1)
    username = factory.Faker('name')
    email = factory.LazyAttribute(lambda o: '%s@example.com' % o.username)