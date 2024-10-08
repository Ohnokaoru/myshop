from django.urls import path
from . import views

urlpatterns = [
    path("add-cart/<int:product_id>/", views.add_cart, name="add-cart"),
    path("view-cart/", views.view_cart, name="view-cart"),
    path("edit-cart/<int:product_id>/", views.edit_cart, name="edit-cart"),
]
