from django.urls import path, include
from . import views


urlpatterns = [
    path("confirm-order/", views.confirm_order, name="confirm-order"),
    path("view-order/", views.view_order, name="view-order"),
]
