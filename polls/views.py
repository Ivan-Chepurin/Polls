from django.views.generic import DetailView, ListView

from .models import Poll, Question
from .utils import QuestionViewMixin, ModelProperties


class PollsHome(ListView):
    model = Poll
    context_object_name = 'polls'
    template_name = 'polls/polls_home_list.html'
    queryset = Poll.objects.filter(visible=True).select_related()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Опросы'
        return context


class PollDetail(DetailView, ModelProperties):
    model = Poll
    context_object_name = 'poll'
    template_name = 'polls/poll_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['number_questions'] = Question.objects.filter(poll=self.object).count()
        start = self.get_next_question_or_none(poll=self.object,
                                               user=self.get_anon_user_object(self.request))
        if start:
            context['start'] = start
        else:
            context['result'] = '/result/{}'.format(self.object.pk)
            context['postscript'] = True
        return context


class QuestionView(QuestionViewMixin):
    '''look at the object in utils.py'''

    def get_success_url(self):
        url = self.get_next_question_or_none(self.poll, self.anon_user_obj)
        if url:
            url = url.get_absolute_url()
            print('url', url)
            return url
        else:
            return '/result/{}'.format(self.poll.pk)


class ResultOfPoll(DetailView, ModelProperties):
    ''
    model = Poll
    template_name = 'polls/poll_results.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.anon_user_obj:
            self.set_anon_user_object(request)
        if not self.poll:
            self.poll = self.get_poll(poll_pk=self.kwargs['pk'])
        if not self.question_choice_answer_set:
            self.set_question_choice_answer_set(self.poll, self.anon_user_obj)

        self.result_dict = self.get_result_dict()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if self.poll:
            return self.poll
        else:
            return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result_dict'] = self.result_dict
        context['title'] = self.poll.title
        return context
