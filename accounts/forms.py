from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from allauth.account.forms import AddEmailForm
from django.core.mail import send_mail
from django import forms
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=get_user_model()
        fields = (
            "email",
            "username",
        )
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "username",
        )
class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            "password",
        )
