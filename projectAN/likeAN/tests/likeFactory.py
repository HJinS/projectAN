import factory

from pytz import timezone
from AN.tests.productFactory import ProductFactory
from socialUser.tests.userFactory import UserFactory
from ..models import LikeProduct

class LikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LikeProduct
    user_id = factory.SubFactory(UserFactory)
    product_id = factory.SubFactory(ProductFactory)