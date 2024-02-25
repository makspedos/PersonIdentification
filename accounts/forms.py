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


# class CustomAddEmailForm(AddEmailForm):
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request', None)
#         super().__init__(*args, **kwargs)
#
#     def save(self):
#         email = self.cleaned_data['email']
#         if self.request and self.request.user:
#             old_email = self.request.user.email
#
#             self.request.user.email = email
#             self.request.user.save()
#
#             send_mail(
#                 'Change of Email Address',
#                 f'Your email address has been changed from {old_email} to {email}.',
#                 'from@example.com',
#                 [old_email],
#                 fail_silently=True,
#             )