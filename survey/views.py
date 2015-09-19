from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import uuid
from django.db import transaction
from rest_framework import status
import rest_framework.response
from .serializers import SurveySerializer, QuestionSerializer, ResponseSerializer, UserSerializer, AnswerSerializer
from .models import Survey, Question, User, Response, Answer
from django.core.exceptions import ValidationError

class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    def post(self, request, *args, **kwargs):
        survey = self.get_object()
        data = request.data
        user = request.user
        with transaction.atomic():
            resp = Response(survey=survey, user=user, uuid=uuid.uuid4().hex)
            resp.save()

            for field_name, field_value in data.items():
                if field_name.startswith("question_"):
                    question_label = field_name.split("_")[1]
                    print(question_label)
                    question = Question.objects.get(label=question_label, survey=survey)
                    answer = Answer(question=question)
                    answer.body = field_value
                    answer.response = resp
                    try:
                        answer.clean()
                    except ValidationError as e:
                        print(field_name, field_value, question.question_type)
                        return rest_framework.response.Response(status=status.HTTP_400_BAD_REQUEST)
                    answer.save()
            resp_serializer = ResponseSerializer(resp, context={"request":request})

            return rest_framework.response.Response(resp_serializer.data, status=status.HTTP_201_CREATED)

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
