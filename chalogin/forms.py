from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField


class ChaloginForm(AuthenticationForm):
    captcha = CaptchaField()
