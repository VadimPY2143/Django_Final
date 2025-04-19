from Auth.models import CreateUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField
from django import forms


class CustomUserCreationForm(forms.ModelForm):
    # captcha = CaptchaField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CreateUser
        fields = ['username', 'email', 'phone_number', 'avatar']


class CustomAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField()

    class Meta:
        fields = ['username', 'password']
