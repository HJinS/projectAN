from rest_framework.test import APIClient, APITestCase
import factory, pytz, uuid

from datetime import datetime
from pytz import timezone
from AN.tests.productFactory import ProductFactory
from ..models import PriceInfo

class PriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PriceInfo
        django_get_or_create = ('id', )
    id = factory.LazyAttribute(lambda _: uuid.uuid4())
    product_id = factory.SubFactory(ProductFactory)
    price = factory.fuzzy.FuzzyFloat(10.8, 3000.24)
    updated_dt = factory.fuzzy.FuzzyDateTime(datetime(2018, 1, 1, tzinfo=timezone('Asia/Seoul')))