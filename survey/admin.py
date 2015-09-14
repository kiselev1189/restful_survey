from django.contrib import admin
from survey.models import Survey, Response, Question, Answer

class QuestionInline(admin.TabularInline):
    model = Question

class AnswerInline(admin.StackedInline):
    model = Answer
    fields = ("question", "body")

class SurveyAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


class ResponseAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    fields = ("survey", "uuid", "user")


admin.site.register(Survey, SurveyAdmin)

admin.site.register(Response, ResponseAdmin)