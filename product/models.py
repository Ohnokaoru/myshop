from django.db import models

# Create your models here.


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_price = models.IntegerField(default=0)
    product_img = models.ImageField(upload_to="product_images/", null=True, blank=True)
    product_description = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.product_name} {self.product_price}"
