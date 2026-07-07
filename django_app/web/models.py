from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class ImageFaces(models.Model):
    """Original image saved by a user for later review."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to="faces_dataset/")

    def __str__(self):
        """Return the owner identifier for admin/debug display."""
        return str(self.user)


class Identification(models.Model):
    """Prediction result for one detected face in a saved image."""

    EMOTION_CHOICES = (
        ("anger", "Anger"),
        ("happy", "Happy"),
        ("neutral", "Neutral"),
        ("sad", "Sad"),
        ("surprise", "Surprise"),
        ("not_selected", "Not selected"),
    )
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("not_selected", "Not selected"),
    )
    image_face = models.ForeignKey(ImageFaces, on_delete=models.CASCADE)
    age = models.IntegerField(default=None, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default="not_selected", blank=True, null=True)
    emotion = models.CharField(max_length=20, choices=EMOTION_CHOICES, default="not_selected", blank=True, null=True)
    face_number = models.IntegerField(default=1)