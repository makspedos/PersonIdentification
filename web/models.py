from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

class ImageFaces(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to=r'C:\Users\maksim\PycharmProjects\face_recognision\media\faces_dataset')


    def __str__(self):
        return self.user.__str__()

class Identification(models.Model):
    EMOTION_CHOICES = (
        ('Злість', 'Злість'),
        ('Радість', 'Радість'),
        ('Нейтральність', 'Нейтральність'),
        ('Сум', 'Сум'),
        ('Здивованість', 'Здивованість'),
        ('Не задано', 'Не задано')
    )
    GENDER_CHOICES = (
        ('Чоловік', 'Чоловік'),
        ('Жінка', 'Жінка'),
        ('Не задано','Не задано')

    )
    image_face = models.ForeignKey(ImageFaces, on_delete=models.CASCADE)
    age = models.IntegerField(default=None, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Не задано', blank=True, null=True)
    emotion = models.CharField(max_length=20, choices=EMOTION_CHOICES, default='Не задано', blank=True, null=True)
    face_number = models.IntegerField(default=1)