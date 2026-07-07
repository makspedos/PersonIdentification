from django.contrib.auth import get_user_model
from django.test import TestCase

from web.models import Identification, ImageFaces


User = get_user_model()


class WebModelTests(TestCase):
    def test_image_faces_string_uses_user(self):
        user = User.objects.create_user(email="user@gmail.com", username="user", password="test")
        image = ImageFaces.objects.create(user=user, img="faces_dataset/family.jpg")
        self.assertEqual(str(image), str(user))

    def test_identification_defaults(self):
        user = User.objects.create_user(email="user@gmail.com", username="user", password="test")
        image = ImageFaces.objects.create(user=user, img="faces_dataset/family.jpg")
        identification = Identification.objects.create(image_face=image)
        self.assertEqual(identification.gender, "not_selected")
        self.assertEqual(identification.emotion, "not_selected")
        self.assertEqual(identification.face_number, 1)