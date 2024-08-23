from django.urls import path
from . import views

urlpatterns = [
    path("create-product/", views.create_product, name="create-product"),
    # path("view-detailproduct/", views.view_detailproduct, name="view-detailproduct"),
    # 會判斷是否為staff而進入不同index
    path("index/", views.index, name="index"),
    path("", views.index, name="index"),
    path("edit-product/<int:product_id>/", views.edit_product, name="edit-product"),
    path(
        "delete-product/<int:product_id>/", views.delete_product, name="delete-product"
    ),
]
