from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


text_validator = RegexValidator(regex=r'^')
phone_validator = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")



class Survey(models.Model):     # collection of unique questions
    name = models.CharField(max_length=400)
    description = models.TextField()


class Question(models.Model):       # linked to it's survey
    PHONE = 'phone'
    TEXT = 'text'

    QUESTION_TYPES = (
        (TEXT, 'text'),
        (PHONE, 'phone')
    )

    QUESTION_VALIDATORS = {
        TEXT: text_validator,
        PHONE: phone_validator
    }

    question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)
    text = models.TextField()
    survey = models.ForeignKey(Survey, related_name='questions')
    label = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        super(Question, self).save(*args, **kwargs)


class Response(models.Model):       # questions + answers + unique id
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    survey = models.ForeignKey(Survey)
    user = models.ForeignKey(User)
    uuid = models.CharField(max_length=32)

class Answer(models.Model):
    question = models.ForeignKey(Question)
    response = models.ForeignKey(Response, related_name='answers')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    body = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        validator = Question.QUESTION_VALIDATORS[self.question.question_type]
        validator(self.body)
        super(Answer, self).save(*args, **kwargs)


