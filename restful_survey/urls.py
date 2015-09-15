"""restful_survey URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from survey import urls as survey_urls
from rest_framework import routers
from survey import views
router = routers.DefaultRouter()
router.register('survey_list', views.SurveyViewSet)
router.register('question_list', views.QuestionViewSet)
router.register('response_list', views.ResponseViewSet, base_name='Response')
router.register('user_list', views.UserViewSet)
router.register('answer_list', views.AnswerViewSet)
survey_app_router = router

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(survey_app_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
