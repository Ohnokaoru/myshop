from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):

    # 定義表單的配置選項
    class Meta:
        model = UserProfile

        exclude = ("user",)
