from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_time = models.DateTimeField(auto_now_add=True)
    total_amount = models.PositiveIntegerField(default=0)
    status_choices = [
        ("panding", "未付款"),
        ("complated", "付款完成"),
        ("cancelled", "取消"),
    ]
    status = models.CharField(max_length=20, choices=status_choices)
    shipping_address = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} {self.total_amount} {self.status}"
