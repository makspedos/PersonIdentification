import os
from django.test import TestCase, Client
from django.urls import reverse
from web.models import Image
# Create your tests here.
class TestViews(TestCase):
    def SetUp(self):
        self.client = Client()

    def test_1(self):
        response = self.client.get(reverse('web:test'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/test.html')
        self.assertContains(response, 'Hello')

    def test_form(self):
        response = self.client.get(reverse('web:form'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/form.html')
        test_image = open(r'C:\Users\maksp\PycharmProjects\face_recognision\media\images\лаб1.png', 'rb')
        form_data = {
            'img':test_image,
        }
        response = self.client.post(reverse('web:home'), data=form_data, format='multipart')
        self.assertTemplateUsed(response, 'html/home.html')
        self.assertEquals(response.status_code, 200)







