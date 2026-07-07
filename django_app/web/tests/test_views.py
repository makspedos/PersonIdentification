from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse


User = get_user_model()


class WebViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email="user@gmail.com", username="user", password="test")
        self.media_root = TemporaryDirectory()
        self.settings_override = override_settings(MEDIA_ROOT=self.media_root.name)
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)
        self.addCleanup(self.media_root.cleanup)

    def test_home_view_renders(self):
        response = self.client.get(reverse("web:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "html/all/home.html")

    def test_help_view_renders(self):
        response = self.client.get(reverse("web:help"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "html/all/help.html")

    @patch("web.views.download_image", return_value=True)
    def test_form_view_stores_selected_params_and_image_url(self, mock_download_image):
        response = self.client.post(
            reverse("web:form_page"),
            data={
                "age": "true",
                "gender": "true",
                "emotion": "true",
                "image_url": "https://example.com/face.jpg",
            },
        )

        self.assertRedirects(response, reverse("web:work_page"), fetch_redirect_response=False)
        self.assertEqual(
            self.client.session["params"],
            {"age": "true", "gender": "true", "emotion": "true"},
        )
        self.assertIn("image_path", self.client.session["img"])
        mock_download_image.assert_called_once()

    def test_work_view_redirects_without_session_input(self):
        response = self.client.get(reverse("web:work_page"))
        self.assertRedirects(response, reverse("web:form_page"), fetch_redirect_response=False)

    @patch("web.views.get_prediction_model")
    def test_work_view_handles_failed_detection(self, mock_get_model):
        self.client.login(email="user@gmail.com", password="test")
        model = Mock()
        model.face_detection.return_value = False
        mock_get_model.return_value = model
        session = self.client.session
        session["params"] = {"age": "true", "gender": None, "emotion": None}
        session["img"] = {"image_path": "unused.png"}
        session.save()

        response = self.client.get(reverse("web:work_page"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "html/all/work_page.html")
        self.assertContains(response, "The image could not be recognized")

    @patch("web.views.get_prediction_model")
    def test_work_view_renders_prediction_table(self, mock_get_model):
        self.client.login(email="user@gmail.com", password="test")
        model = Mock()
        model.face_detection.return_value = (
            [{"age": 20, "gender": "male", "emotion": ["10.0", "20.0", "30.0", "25.0", "15.0"]}],
            ["age", "gender", "emotion"],
        )
        mock_get_model.return_value = model
        session = self.client.session
        session["params"] = {"age": "true", "gender": "true", "emotion": "true"}
        session["img"] = {"image_path": "unused.png"}
        session.save()

        response = self.client.get(reverse("web:work_page"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "html/all/work_page.html")
        self.assertContains(response, "Predictions")
        self.assertContains(response, "male")
        self.assertContains(response, "20")