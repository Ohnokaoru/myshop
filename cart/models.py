from django.db import models

# Create your models here.

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from product.models import Product


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    # 模型內部的配置類
    class Meta:
        unique_together = ("user", "product")

    # 如果有同一使用者新增同一商品會引起錯誤
    def save(self, *args, **kwargs):
        if CartItem.objects.filter(user=self.user, product=self.product).exists():
            raise ValidationError("")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} {self.quantity}"
