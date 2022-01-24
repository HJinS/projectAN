from tkinter import CASCADE
from djongo import models
from socialUser.models import User
from AN.models import Product

class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)