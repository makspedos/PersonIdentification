from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .forms import *
from django.urls import reverse, resolve
from .views import SignUpPageView

# Create your tests here.
class TestUserCreation(TestCase):
    def SetUp(self):
        self.client = Client()

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="user@gmail.com",username="user",password="test")
        self.assertEqual(user.username, "user")
        self.assertEqual(user.email,"user@gmail.com")
        self.assertFalse(user.is_superuser)

    def test_login_template(self):
        response = self.client.get("/account/login/")
        self.assertTemplateUsed(response, "registration/login.html")

    def test_signup_template(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_form(self):
        response = self.client.get(reverse("signup"))
        form = response.context.get('form')
        self.assertIsInstance(form, CustomUserCreationForm)

    def test_signup_view(self):
        view = resolve("/account/signup/")
        self.assertEqual(view.func.__name__, SignUpPageView.as_view().__name__)
