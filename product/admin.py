from django.contrib import admin


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_name",
        "product_price",
    )
    list_filter = ("id", "product_name")
    search_fields = ("product_name",)
    ordering = ("id",)


admin.site.register("Product", "ProductAdmin")
