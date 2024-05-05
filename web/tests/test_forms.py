from django.test import TestCase
from web import forms

class TestForm(TestCase):
    def test_face_form(self):
        form_data = {'img': 'C:/Users/maksp/Downloads/family.jpg', 'url':None}
        form_data = forms.FaceForm(data=form_data)
        self.assertTrue(form_data.is_valid())
