from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import *
from .apiviews import PollViewSet, QuestionViewSet

router = DefaultRouter()
router.register(r'polls', PollViewSet)
router.register(r'questions', QuestionViewSet)

# api_urlpatterns = [
#     path('', api_root),
#     path('polls/', PollsViewSet.as_view({'get': 'list'}), name='polls-list'),
#     path('polls/<int:pk>', PollsViewSet.as_view({'get': 'retrieve'}), name='poll-detail'),
#     path('question/<int:pk>', QuestionViewSet.as_view({'get': 'retrieve', 'post': 'create'}), name='question-detail'),
#     # path('test/<int:pk>', QuestionGenericAPIView.as_view(), name='test')
#     # path('question/<int:pk>/answer/', AnswerCreateAPIView.as_view(), name='answer-create')
# ]

site_urlpatterns = [
    path('', PollsHome.as_view(), name='polls_home'),
    path('poll/<int:pk>', PollDetail.as_view(), name='view_poll'),
    path('question/<int:pk>', QuestionView.as_view(), name='view_question'),
    path('result/<int:pk>', ResultOfPoll.as_view(), name='result'),
]


urlpatterns = [
    path('', include(site_urlpatterns)),
    path('api/', include(router.urls)),
]
