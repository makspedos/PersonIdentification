from django.test import TestCase, Client
from django.urls import reverse

class TestViews(TestCase):
    def SetUp(self):
        self.client = Client()

    def test_help_view(self):
        response = self.client.get(reverse('web:help'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/all/help.html')

    def test_home_view(self):
        response = self.client.get(reverse('web:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/all/home.html')

    def test_form_view(self):
        response = self.client.get(reverse('web:form_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/all/form.html')