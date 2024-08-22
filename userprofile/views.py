from django.shortcuts import render
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required

# Create your views here.


# 建立個人資料
@login_required
def create_userprofile(request):
    message = ""
    userprofileform = None

    if request.method == "POST":
        form = UserProfileForm(request.POST)
        if form.is_valid():
            userprofileform = form.save(commit=False)
            userprofileform.user = request.user
            userprofileform.save()
            message = "建立個人資訊成功"

        else:
            message = "資料錯誤"
    else:
        form = UserProfileForm()

    return render(
        request,
        "userprofile/create-userprofile.html",
        {"form": form, "userprofileform": userprofileform, "message": message},
    )
