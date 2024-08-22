from django.urls import path
from . import views

urlpatterns = [path("chalogin/", views.chalogin, name="chalogin")]
