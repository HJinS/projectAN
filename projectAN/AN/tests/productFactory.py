import factory, pytz, uuid
import factory.fuzzy

from ..models import Product
from datetime import datetime
from pytz import timezone

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        django_get_or_create = ('id', )
    id = factory.LazyAttribute(lambda _: uuid.uuid4())
    name = factory.Faker('sentence')
    img_src = factory.Faker('url')
    site = factory.fuzzy.FuzzyInteger(0, 1)
    category = factory.fuzzy.FuzzyChoice(["intel cpu", "amd cpu", "radeon gpu", "nvidia gpu", "ddr4 ram", "ddr5 ram", "nvme ssd", "sata ssd", "liquid cpu cooler", "air cpu cooler"])
    updated_dt = factory.fuzzy.FuzzyDateTime(datetime(2018, 1, 1, tzinfo=timezone('Asia/Seoul')))