from django.db import models
from django.contrib.auth.models import User
from product.models import Product

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)
    total_amount = models.PositiveIntegerField(default=0)
    status_choices = [
        ("pending", "未付款"),
        ("completed", "付款完成"),
        ("cancelled", "取消"),
    ]
    status = models.CharField(max_length=20, choices=status_choices)
    shipping_address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} {self.total_amount} {self.status}"


# 管理訂單中的商品，轉移購物車內商品用
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"訂單:{self.order.id} 商品:{self.product.product_name} 數量:{self.quantity}"
