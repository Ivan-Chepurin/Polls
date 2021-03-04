from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets

from .models import Poll, Question, Answer
from .utils import ModelProperties
from .serializers import PollSerializer, QuestionSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'polls': reverse('polls-list', request=request, format=format)
    })


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class QuestionViewSet(viewsets.ModelViewSet, ModelProperties):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def dispatch(self, request, *args, **kwargs):
        print(request.__dict__)
        self.user_id = self.get_anon_user_object(request)
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user_id'] = self.user_id
        print(context)

        if 'pk' in self.kwargs:
            context['object'] = self.get_object()
        return context


