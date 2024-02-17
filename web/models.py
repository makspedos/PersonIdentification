# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
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
