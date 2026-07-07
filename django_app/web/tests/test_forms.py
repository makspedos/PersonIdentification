from django.test import TestCase

from web.forms import FaceForm


class TestForm(TestCase):
    def test_face_form_accepts_url(self):
        form = FaceForm(data={"image_url": "https://example.com/family.jpg"})
        self.assertTrue(form.is_valid())

    def test_face_form_requires_image_or_url(self):
        form = FaceForm(data={})
        self.assertFalse(form.is_valid())