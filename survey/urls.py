__author__ = 'kis'
from rest_framework.routers import DefaultRouter
from survey import views

router = DefaultRouter()
router.register('survey_list', views.SurveyViewSet)
router.register('question_list', views.QuestionViewSet)
router.register('response_list', views.ResponseViewSet, base_name='Response')
router.register('user_list', views.UserViewSet)
router.register('answer_list', views.AnswerViewSet)
survey_app_router = router
