from rest_framework.test import APIClient, APITestCase
import factory, pytz, uuid
from ..models import Product

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    