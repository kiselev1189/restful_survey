__author__ = 'kis'
from rest_framework import serializers
from .models import Survey, Question, User, Response, Answer

class SurveySerializer(serializers.HyperlinkedModelSerializer):
    questions = serializers.HyperlinkedRelatedField(many=True, view_name='question-detail', read_only=True)

    class Meta:
        model = Survey
        fields = ('name', 'description', 'questions')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    survey = serializers.HyperlinkedRelatedField(many=False, view_name='survey-detail', read_only=True)

    class Meta:
        model = Question
        fields = ('question_type', 'text', 'survey', 'label')

class ResponseSerializer(serializers.HyperlinkedModelSerializer):
    survey = serializers.HyperlinkedRelatedField(many=False, view_name='survey-detail', read_only=True)
    user = serializers.HyperlinkedRelatedField(many=False, view_name='user-detail', read_only=True)
    answers = serializers.HyperlinkedRelatedField(many=True, view_name='answer-detail', read_only=True)

    class Meta:
        model = Response
        fields = ('created', 'updated', 'survey', 'user', 'uuid', 'answers')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ("username",)


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    response = serializers.HyperlinkedRelatedField(many=False, view_name='Response-detail', read_only=True)

    class Meta:
        model = Answer
        fields = ('question', 'response', 'created', 'body')