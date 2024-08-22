from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    name = models.CharField(max_length=20)
    gender_choices = [("M", "男"), ("F", "女")]
    gender = models.CharField(max_length=1, choices=gender_choices)
    birthday = models.DateField()
    email = models.EmailField()
    tel = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


def __str__(self):
    return f"{self.name} {self.email} {self.address}"
