from django.contrib import admin
from .models import Product


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_name",
        "product_price",
        "product_img",
        "product_stock",
    )
    list_filter = ("id", "product_name")
    search_fields = ("product_name",)
    ordering = ("id",)

    def product_img(self, obj):
        if obj.product_img:
            return f'<img src="{obj.product_img.url}" width="100" />'
        return "No Image"

    product_img.allow_tags = True


admin.site.register(Product, ProductAdmin)
