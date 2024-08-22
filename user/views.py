from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def user_register(request):
    message = ""

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

        else:
            message = "資料錯誤"

    else:
        form = UserCreationForm()

    return render(
        request, "user/user-register.html", {"form": form, "message": message}
    )
