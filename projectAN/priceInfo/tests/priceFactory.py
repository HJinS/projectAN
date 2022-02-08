from rest_framework.test import APIClient, APITestCase
import factory, pytz, uuid

from AN.tests.productFactory import ProductFactory
from ..models import PriceInfo

class PriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PriceInfo
    product_id = factory.SubFactory(ProductFactory)