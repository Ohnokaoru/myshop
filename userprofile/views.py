from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def view_userprofile(request):
    try:
        userprofile = UserProfile.objects.get(user=request.user)

    except UserProfile.DoesNotExist:
        return redirect("create-userprofile")

    return render(
        request, "userprofile/view-userprofile.html", {"userprofile": userprofile}
    )


# 建立個人資料
@login_required
def create_userprofile(request):
    message = ""

    if request.method == "POST":
        form = UserProfileForm(request.POST)

        if form.is_valid():
            userprofileform = form.save(commit=False)
            userprofileform.user = request.user
            userprofileform.save()
            return redirect("view-userprofile")

        else:
            message = "資料錯誤"
    else:
        form = UserProfileForm()

    return render(
        request,
        "userprofile/create-userprofile.html",
        {"form": form, "message": message},
    )


# 修改個人資料
@login_required
def edit_userprofile(request):
    message = ""

    try:
        userprofile = UserProfile.objects.get(user=request.user)

    except UserProfile.DoesNotExist:
        return redirect("create-userprofile")

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=userprofile)

        if form.is_valid():
            userprofileform = form.save(commit=False)
            userprofileform.user = request.user
            userprofileform.save()
            return redirect("view-userprofile")

        else:
            message = "資料錯誤"

    else:
        form = UserProfileForm(instance=userprofile)

    return render(
        request,
        "userprofile/edit-userprofile.html",
        {"message": message, "form": form},
    )
