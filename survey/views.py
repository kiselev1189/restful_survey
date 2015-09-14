from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import SurveySerializer, QuestionSerializer, ResponseSerializer, UserSerializer, AnswerSerializer
from .models import Survey, Question, User, Response, Answer
from rest_framework import mixins
from rest_framework import generics
from rest_framework import response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import uuid

class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    def post(self, request, *args, **kwargs):
        survey = self.get_object()
        data = request.data
        user = request.user

        resp = Response(survey=survey, user=user, uuid=uuid.uuid4().hex)
        resp.save()

        for field_name, field_value in data.items():
            if field_name.startswith("question_"):
                question_id = int(field_name.split("_")[1])
                question = Question.objects.get(pk=question_id)

                answer = Answer(question=question)
                answer.body = field_value
                answer.response = resp
                answer.save()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class ResponseViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = list(Response.objects.filter(user=self.request.user))
        return queryset

    serializer_class = ResponseSerializer


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
