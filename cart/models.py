from django.db import models

# Create your models here.

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from product.models import Product


# 加入購物車
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    # 模型內部的配置類
    class Meta:
        # 一個使用者與同一商品只會有一個實體物件，若有多個同樣商品，則quantity增加(在views.py做)
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.product} {self.quantity}"
