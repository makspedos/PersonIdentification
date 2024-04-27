from django.test import TestCase
from accounts import forms


class TestForm(TestCase):
    def test_user_creation(self):
        form_data = {"email": "testuser23@gmail.com", "username": "newuser",
                     'password1':"Testasgaswrts261", 'password2':"Testasgaswrts261"}
        form = forms.UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())