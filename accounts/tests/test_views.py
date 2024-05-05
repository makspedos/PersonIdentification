from allauth.account.models import EmailAddress
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from accounts.views import SignUpPageView

User = get_user_model()


class TestViews(TestCase):
    def setUp(self):
        self.user_1 = User.objects.create_user(email="user@gmail.com", username="user", password="test")
        self.user_1.save()

    def test_login_view(self):
        response = self.client.get("/accounts/login/")
        self.assertTemplateUsed(response, "account/login.html")

    def test_signup_view(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup.html")

        view = resolve("/accounts/signup/")
        self.assertEqual(view.func.__name__, SignUpPageView.as_view().__name__)

    def test_profile_view(self):
        login = self.client.login(email="user@gmail.com", password="test")
        response = self.client.get(reverse('accounts:profile'))

        self.assertEqual(response.context['user'].username, "user")
        self.assertTemplateUsed(response, "account/profile.html")
        self.assertTrue(login)

    def test_change_password_view(self):
        login = self.client.login(email="user@gmail.com", password="test")
        response = self.client.get("/accounts/password/change/")
        self.assertTemplateUsed(response, "account/password_change.html")
        self.assertTrue(login)

    def test_change_username_view(self):
        login = self.client.login(email="user@gmail.com", password="test")
        response = self.client.get(reverse('accounts:username'))
        self.assertTemplateUsed(response, "account/username_change.html")
        self.assertTrue(login)

    def test_change_email_view(self):
        login = self.client.login(email="user@gmail.com", password="test")
        email = EmailAddress.objects.create(user=self.user_1, email="user@gmail.com", verified=True, primary=True)
        email.save()
        data = {"email-add": True, "email": "user1@gmail.com"}
        response = self.client.post(reverse('accounts:email'), data)
        self.assertTrue(EmailAddress.objects.filter(email="user1@gmail.com", primary=True))
        self.assertTrue(EmailAddress.objects.filter(email="user@gmail.com", primary=False))
        self.assertTrue(login)
        self.assertEqual(response.url, reverse('accounts:profile'))

    def test_change_email_blank(self):
        login = self.client.login(email="user@gmail.com", password="test")
        email = EmailAddress.objects.create(user=self.user_1, email="user@gmail.com", verified=True, primary=True)
        email.save()
        data = {"email-add": True, "email": ""}
        response = self.client.post(reverse('accounts:email'), data)
        self.assertFalse(EmailAddress.objects.filter(email=""))
        self.assertEqual(response.url, reverse('accounts:email'))
        self.assertTrue(login)

    def test_delete_email_view(self):
        login = self.client.login(email="user@gmail.com", password="test")
        email = EmailAddress.objects.create(user=self.user_1, email="user@gmail.com", verified=True, primary=True)
        email2 = EmailAddress.objects.create(user=self.user_1, email="user1@gmail.com", verified=True, primary=False)
        email.save()
        email2.save()
        data = {"email-delete": True, "email": "user1@gmail.com"}
        response = self.client.post(reverse('accounts:email'), data)
        self.assertFalse(EmailAddress.objects.filter(email="user1@gmail.com"))
        self.assertTrue(login)
        self.assertEqual(response.url, reverse('accounts:profile'))