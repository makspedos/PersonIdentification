from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import resolve, reverse

from accounts.views import SignUpPageView
from web.models import Identification, ImageFaces


User = get_user_model()


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_1 = User.objects.create_user(email="user@gmail.com", username="user", password="test")

    def test_saved_results_view(self):
        img_face = ImageFaces.objects.create(user=self.user_1, img="faces_dataset/family.jpg")
        Identification.objects.create(image_face=img_face, age=20, gender="female", face_number=1)
        Identification.objects.create(image_face=img_face, age=25, gender="female", face_number=2)
        Identification.objects.create(image_face=img_face, age=40, gender="female", face_number=3)
        Identification.objects.create(image_face=img_face, age=9, gender="female", face_number=4)

        self.client.login(email="user@gmail.com", password="test")
        response = self.client.get(reverse("accounts:results"))

        self.assertTemplateUsed(response, "account/results_page.html")
        self.assertEqual(response.context["dict_results"].get(img_face)[0].age, 20)
        self.assertEqual(response.context["dict_results"].get(img_face)[3].age, 9)
        self.assertContains(response, "female")

    def test_login_view(self):
        data_login = {"login": "user@gmail.com", "password": "test"}
        response = self.client.post("/accounts/login/", data=data_login)
        self.assertEqual(response.url, reverse("web:form_page"))
        self.assertTrue(response.context["user"].is_authenticated)
        self.assertEqual(response.status_code, 302)

    def test_signup_view(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/signup.html")

        view = resolve("/accounts/signup/")
        self.assertEqual(view.func.__name__, SignUpPageView.as_view().__name__)

    def test_profile_view(self):
        login = self.client.login(email="user@gmail.com", password="test")
        response = self.client.get(reverse("accounts:profile"))
        self.assertNotEqual(response.context["user"].username, "notuser")
        self.assertTemplateUsed(response, "account/profile.html")
        self.assertTrue(login)

    def test_change_password_view(self):
        login = self.client.login(email="user@gmail.com", password="test")
        response = self.client.get("/accounts/password/change/")
        self.assertTemplateUsed(response, "account/password_change.html")
        self.assertTrue(login)

    def test_change_username_view(self):
        login = self.client.login(email="user@gmail.com", password="test")
        response = self.client.get(reverse("accounts:username"))
        self.assertTemplateUsed(response, "account/username_change.html")
        self.assertTrue(login)

    def test_change_email_view(self):
        login = self.client.login(email="user@gmail.com", password="test")
        EmailAddress.objects.create(user=self.user_1, email="user@gmail.com", verified=True, primary=True)
        data = {"email-add": True, "email": "user1@gmail.com"}
        response = self.client.post(reverse("accounts:email"), data)
        self.assertTrue(EmailAddress.objects.filter(email="user1@gmail.com", primary=True))
        self.assertTrue(EmailAddress.objects.filter(email="user@gmail.com", primary=False))
        self.assertTrue(login)
        self.assertEqual(response.url, reverse("accounts:profile"))

    def test_change_email_blank(self):
        login = self.client.login(email="user@gmail.com", password="test")
        EmailAddress.objects.create(user=self.user_1, email="user@gmail.com", verified=True, primary=True)
        data = {"email-add": True, "email": ""}
        response = self.client.post(reverse("accounts:email"), data)
        self.assertFalse(EmailAddress.objects.filter(email=""))
        self.assertEqual(response.url, reverse("accounts:email"))
        self.assertTrue(login)

    def test_delete_email_view(self):
        login = self.client.login(email="user@gmail.com", password="test")
        EmailAddress.objects.create(user=self.user_1, email="user@gmail.com", verified=True, primary=True)
        EmailAddress.objects.create(user=self.user_1, email="user1@gmail.com", verified=True, primary=False)
        data = {"email-delete": True, "email": "user1@gmail.com"}
        response = self.client.post(reverse("accounts:email"), data)
        self.assertFalse(EmailAddress.objects.filter(email="user1@gmail.com"))
        self.assertTrue(login)
        self.assertEqual(response.url, reverse("accounts:profile"))