from django.db.models.constraints import UniqueConstraint
from django.db import models
import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    product_id = models.CharField(max_length=40)
    name = models.CharField(max_length=300)
    price = models.CharField(max_length=16)
    img_src = models.URLField(max_length=100)
    category = models.CharField(max_length=18)
    site = models.PositiveSmallIntegerField()
    updated_dt = models.DateField(auto_now=True)
    
    class Meta:
        UniqueConstraint(fields=['product_id, updated_dt'], name='id_date_constraint')
        verbose_name = "Crawl_Product_Info"