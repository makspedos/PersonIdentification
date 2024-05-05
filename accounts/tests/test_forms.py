from django.contrib.auth import get_user_model
from django.test import TestCase
from accounts import forms

User = get_user_model()


class TestForm(TestCase):
    def test_user_creation(self):
        form_data = {"email": "testuser23@gmail.com", "username": "newuser",
                     'password1':"Testasgaswrts261", 'password2':"Testasgaswrts261"}
        form = forms.UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_change_username(self):
        form_data = {"username":"user1"}
        form = forms.CustomUserChangeForm(data=form_data)
        self.assertTrue(form.is_valid())
    def test_change_password(self):
        user_1 = User.objects.create_user(email="user@gmail.com", username="user", password="test")
        user_1.save()
        form_data = {"old_password": "test", "new_password1": "Asghas152asf", "new_password2":"Asghas152asf"}
        form = forms.PasswordChangeForm(user=user_1,data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        updated_user = User.objects.get(email="user@gmail.com")
        self.assertTrue(updated_user.check_password("Asghas152asf"))


