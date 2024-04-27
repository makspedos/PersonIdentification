from django.contrib.auth import get_user_model
from django.test import TestCase
from allauth.account.models import EmailAddress

class TestModel(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="user@gmail.com", username="user", password="test")
        self.assertEqual(user.username, "user")
        self.assertFalse(user.is_superuser)
        self.assertEqual(User.objects.all()[0].email, user.email)


    def test_create_email(self):
        email = EmailAddress.objects.create()