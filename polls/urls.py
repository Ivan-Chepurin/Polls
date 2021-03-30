from django.urls import path, include


from .views import PollDetail, QuestionView, ResultOfPoll


urlpatterns = [
    path('', PollsHome.as_view(), name='polls_home'),
    path('poll/<int:pk>', PollDetail.as_view(), name='view_poll'),
    path('question/<int:pk>', QuestionView.as_view(), name='view_question'),
    path('result/<int:pk>', ResultOfPoll.as_view(), name='result'),
]
