from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.forms import CustomPasswordChangeForm, CustomUserChangeForm, CustomUserCreationForm


User = get_user_model()


class AccountFormTests(TestCase):
    def test_user_creation_form_is_valid(self):
        form = CustomUserCreationForm(
            data={
                "email": "testuser23@gmail.com",
                "username": "newuser",
                "password1": "StrongPass261!",
                "password2": "StrongPass261!",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_change_username_form_is_valid(self):
        form = CustomUserChangeForm(data={"username": "user1"})
        self.assertTrue(form.is_valid(), form.errors)

    def test_change_password_form_updates_password(self):
        user = User.objects.create_user(email="user@gmail.com", username="user", password="OldPass261!")
        form = CustomPasswordChangeForm(
            user=user,
            data={
                "old_password": "OldPass261!",
                "new_password1": "NewPass261!",
                "new_password2": "NewPass261!",
            },
        )
        self.assertTrue(form.is_valid(), form.errors)
        form.save()
        user.refresh_from_db()
        self.assertTrue(user.check_password("NewPass261!"))