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

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('confirm_password'):
            self.add_error('confirm_password', "Passwords must match")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField()

    class Meta:
        fields = ['username', 'password']
