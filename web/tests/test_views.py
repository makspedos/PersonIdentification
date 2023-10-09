from django.test import TestCase, Client
from django.urls import reverse
# Create your tests here.
class TestViews(TestCase):
    def SetUp(self):
        self.client = Client()

    def test_1(self):
        response = self.client.get(reverse('web:test'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/home.html')
        self.assertContains(response, 'Hello')





