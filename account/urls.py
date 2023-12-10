from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", SignUpPageView.as_view(), name="signup"),
]