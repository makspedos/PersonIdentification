from unittest.mock import Mock, patch, MagicMock

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

import web.views

User = get_user_model()


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_1 = User.objects.create_user(email="user@gmail.com", username="user", password="test")
        self.user_1.save()

    def test_form_view(self):
        form_data = {
            "вік": "true",
            "стать": "true",
            "емоції": "true",
        }
        response = self.client.post(reverse('web:form_page'), data=form_data)

        self.assertEqual(self.client.session['params'], {"вік": "true", "стать": "true", "емоції": "true"})
        self.assertEqual(response.status_code, 302)


    def test_help_view(self):
        response = self.client.get(reverse('web:help'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/all/help.html')

    def test_home_view(self):
        login = self.client.login(email="user@gmail.com", password="test")
        response = self.client.get(reverse('web:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/all/home.html')
        self.assertEqual(str(response.context['user']), str(self.user_1))
        self.assertTrue(login)


    @patch("web.views.PredictionModel.face_detection")
    def test_work_view(self, mock_result):
        login = self.client.login(email="user@gmail.com", password="test")
        mock_result.return_value = False

        mock_params = Mock()
        mock_cols = Mock()
        expected_result = False
        actual_result = web.views.PredictionModel.face_detection(mock_params, mock_cols)
        print(actual_result)
        assert actual_result ==expected_result

        response = self.client.get(reverse("web:work_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/all/work_page.html')
        # [{'вік':None,'стать':None, 'емоції':None}],["вік", 'стать', 'емоції']

