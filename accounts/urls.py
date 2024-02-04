from django.urls import path
from .views import *

app_name="accounts"

urlpatterns = [
    path("signup/", SignUpPageView.as_view(), name="signup"),
    path("profile/", AccountProfileView.as_view(), name="profile"),
    path("change_username/", AccountChangeUsername.as_view(), name="username"),
]