from rest_framework.test import APIClient, APITestCase
import factory, pytz, uuid
from ..models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User