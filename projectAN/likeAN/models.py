from tkinter import CASCADE
from django.db import models
from socialUser.models import User
from AN.models import Product

class LikeProduct(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likeRelate')
    
    class Meta:
        db_table = 'likeAN'
        constraints = [models.UniqueConstraint(fields=['user_id', 'product_id'], name='likeConstraints')]