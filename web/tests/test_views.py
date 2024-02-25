from ..models import *
from django.test import TestCase, Client
from django.urls import reverse
from web.models import Image
# Create your tests here.


class TestViews(TestCase):
    def SetUp(self):
        self.client = Client()

    def test_models_help(self):
        questions = Question.objects.create(text_question='How to start system?')
        answer = Answer.objects.create(text_answer='Answer', question=questions)
        self.assertEqual(answer.question_id, questions.id)

    def test_help_view(self):
        response = self.client.get(reverse('web:help'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'html/all/help.html')