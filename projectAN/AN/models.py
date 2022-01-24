from django.db.models.constraints import UniqueConstraint
from djongo import models

class Product(models.Model):
    id = models.UUIDField(primary_key=True)
    product_id = models.CharField(max_length=26)
    name = models.CharField(max_length=300)
    price = models.CharField(max_length=8)
    img_src = models.URLField(max_length=30)
    category = models.CharField(max_length=12)
    site = models.PositiveSmallIntegerField()
    updated_dt = models.DateField(auto_now=True)
    
    class Meta:
        UniqueConstraint(fields=['product_id, updated_dt'], name='id_date_constraint')
        verbose_name = "Crawl_Product_Info"