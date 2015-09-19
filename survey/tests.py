from django.test import TestCase
from django.test import Client
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
import factory
from django.contrib.auth.models import User
from rest_framework import status
from .models import Survey, Question, Answer, Response



class SurveyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Survey
        django_get_or_create = ("name",)

    name = 'Default Survey Name'
    description = "Default Survey Description"


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Question

    survey = factory.SubFactory(SurveyFactory)
    question_type = Question.TEXT
    text = "Default question text?"
    label = factory.Sequence(lambda n: "question_" + str(n) )




class SurveyTestCase(APITestCase):
    def setUp(self):
        self.survey = SurveyFactory()
        # get 3 phone fields, 3 text fields

        question_text = QuestionFactory(survey=self.survey, question_type=Question.TEXT, label="question_text")
        question_phone = QuestionFactory(survey=self.survey, question_type=Question.PHONE, label="question_phone")


    def test_respond(self):
        user = User.objects.create_user("default_username", "mail@mail.com", "default_password")

        c = self.client.login(username="default_username", password="default_password")
        payload = {"question_text":"sending some text on question 1...", "question_phone":"+999999999"}
        url = "http://testserver/survey_list/" + str(self.survey.id)
        response = self.client.post(url, payload, format="json")
        print(response)
        self.assertEqual(Response.objects.count(), 1)
        self.assertEqual(Answer.objects.count(), 2)



