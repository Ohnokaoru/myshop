from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import ChaloginForm
from django.contrib.auth import login


# Create your views here.
def chalogin(request):
    message = ""
    if request.method == "POST":
        form = ChaloginForm(request, request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")

        else:
            message = "登入失敗"

    else:
        form = ChaloginForm()

    return render(request, "chalogin/chalogin.html", {"form": form, "message": message})
