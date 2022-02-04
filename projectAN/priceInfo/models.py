from tkinter import CASCADE
from django.db import models
from AN.models import Product
from uuid import uuid4

class PriceInfo(models.Model):
    id = models.UUIDField(default=uuid4, auto_created=True, primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    updated_dt = models.DateField(auto_now=True)
    price = models.FloatField()
    
    class Meta:
        db_table = 'prices'