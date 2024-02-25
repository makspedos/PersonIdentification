from django.db import models


class Image(models.Model):
    img = models.ImageField(upload_to='images/')
    age = models.CharField(max_length=20,null=True, blank=True)
    gender = models.CharField(max_length=20,null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'image'


class Question(models.Model):
    text_question = models.CharField(max_length=150)

    def __str__(self):
        return self.text_question


class Answer(models.Model):
    text_answer = models.CharField(max_length=150)
    question = models.OneToOneField(Question, on_delete= models.CASCADE, default=None)
