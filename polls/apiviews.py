from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets

from .models import Poll, Question, Answer
from .utils import ModelProperties, AnonUserManager
from .serializers import (PollSerializer,
                          QuestionSerializer,
                          AnswerCreateSerializer)


# @api_view(['GET'])
# def api_root(request, format=None):
#     return Response({
#         'polls': reverse('polls-list', request=request, format=format)
#     })


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class QuestionViewSet(viewsets.ModelViewSet, ModelProperties):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def dispatch(self, request, *args, **kwargs):
        self.user_id = self.get_anon_user_object(request)
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.user_id

        if 'pk' in self.kwargs:
            context['object'] = self.get_object()
        return context


class AnswerCreate(viewsets.ModelViewSet, AnonUserManager):
    queryset = Question.objects.all()
    serializer_class = AnswerCreateSerializer

    # def get_serializer_class(self):
    #     return AnswerCreateSerializer

    def dispatch(self, request, *args, **kwargs):
        self.user_id = self.get_anon_user_object(request)
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['question'] = self.get_object()
        print(context['question'])
        context['user_id'] = self.user_id
        return context


