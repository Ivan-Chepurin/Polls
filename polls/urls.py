from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import *
from .apiviews import PollViewSet, QuestionViewSet, AnswerCreate

# router = DefaultRouter()
# router.register(r'polls', PollViewSet)
# router.register(r'questions', QuestionViewSet)

api_urlpatterns = [
    path('polls/', PollViewSet.as_view({'get': 'list'}), name='poll-list'),
    path('polls/<int:pk>', PollViewSet.as_view({'get': 'retrieve'}), name='poll-detail'),
    path('questions/', QuestionViewSet.as_view({'get': 'list'}), name='question-list'),
    path('questions/<int:pk>/', QuestionViewSet.as_view({'get': 'retrieve'}), name='question-detail'),
    path('questions/<int:pk>/answer/', AnswerCreate.as_view({'post': 'create'}), name='answer-create')
]

site_urlpatterns = [
    path('', PollsHome.as_view(), name='polls_home'),
    path('poll/<int:pk>', PollDetail.as_view(), name='view_poll'),
    path('question/<int:pk>', QuestionView.as_view(), name='view_question'),
    path('result/<int:pk>', ResultOfPoll.as_view(), name='result'),
]


urlpatterns = [
    path('', include(site_urlpatterns)),
    path('api/', include(api_urlpatterns)),
    # path('api/', include(router.urls)),
]
