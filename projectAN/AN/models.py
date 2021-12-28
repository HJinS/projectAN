from django.db import models

class product(models.Model):
    id = models.CharField(max_length=26, primary_key=True)
    name = models.CharField(max_length=300)
    price = models.CharField(max_length=8)
    img_src = models.URLField(max_length=30)
    category = models.CharField(max_length=12)
    site = models.PositiveSmallIntegerField()
    updated_dt = models.DateField(auto_now=True)