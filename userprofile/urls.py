from django.urls import path
from . import views

urlpatterns = [
    path("view-userprofile/", views.view_userprofile, name="view-userprofile"),
    path("create-userprofile/", views.create_userprofile, name="create-userprofile"),
    path("edit-userprofile/", views.edit_userprofile, name="edit-userprofile"),
]
