from django.contrib import admin
from .models import UserProfile

# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "birthday", "email", "phone", "address")
    list_filter = ("address",)
    search_fields = ("name", "address", "email", "phone")
    ordering = ("id",)


admin.site.register(UserProfile, UserProfileAdmin)
