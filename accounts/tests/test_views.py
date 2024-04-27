from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from accounts.forms import *
from django.urls import reverse, resolve
from accounts.views import SignUpPageView

class TestUserCreation(TestCase):
    def SetUp(self):
        self.client = Client()

    def test_login_view(self):
        response = self.client.get("/accounts/login/")
        self.assertTemplateUsed(response, "account/login.html")

    def test_signup_view(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup.html")

        view = resolve("/accounts/signup/")
        self.assertEqual(view.func.__name__, SignUpPageView.as_view().__name__)
