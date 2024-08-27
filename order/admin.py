from django.contrib import admin
from .models import Order

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user_username", "order_time", "status")
    list_filter = ("user", "status")
    search_fields = ("user", "order_time", "status")
    ordering = ("order_time",)

    # 取得外鑑關聯資料庫欄位(self為OrderAdmin的實體物件，obj為Order的實體物件)，只能用在list_display
    def user_username(self, obj):
        return obj.user.username


admin.site.register(Order, OrderAdmin)
