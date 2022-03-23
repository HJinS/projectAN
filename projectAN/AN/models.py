from django.db.models.constraints import UniqueConstraint
from django.db import models

class Product(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    name = models.CharField(max_length=300)
    img_src = models.URLField(max_length=100)
    category = models.CharField(max_length=18)
    site = models.PositiveSmallIntegerField()
    updated_dt = models.DateField(auto_now=True)
    
    class Meta:
        db_table = 'product'
        verbose_name = "Crawl_Product_Info"