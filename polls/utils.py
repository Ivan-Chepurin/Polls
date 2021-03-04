from django.views.generic import FormView
from django.contrib.sessions.models import Session
from django.db.models import Prefetch

from django.shortcuts import get_object_or_404

from .models import AnonUserId, Question, Choice, Answer, Poll
from .forms import WritenAnswerForm, OneAnswerForm, MultipleAnswerForm


class AnonUserManager:
    db_model = AnonUserId
    anon_user_obj = None

    def set_anon_user_object(self, request):
        self.anon_user_obj = self.get_anon_user_object(request)

    def get_anon_user_object(self, request):
        session_key = self.get_session(request)
        try:
            anon_user_obj = self.db_model.objects.get(session=session_key)
            return anon_user_obj
        except Exception as e:
            print(e)
            return self.create_anon_user(request)

    def create_anon_user(self, request):
        anon_user_object = self.db_model.objects.create(
            session=Session.objects.get(pk=request.session.session_key))
        anon_user_object.save()
        return anon_user_object

    def get_session(self, request):
        session_key = request.session.session_key
        if session_key:
            return session_key
        else:
            self.create_session(request)
            return request.session.session_key

    def create_session(self, request):
        request.session.cycle_key()
        request.session.set_expiry(5184000)


class PollProperties:
    poll = None

    def set_poll(self, question_obj=None, poll_pk=None):
        if question_obj:
            self.poll = Poll.objects.get(pk=question_obj.poll_id)
        elif poll_pk:
            self.poll = Poll.objects.get(pk=poll_pk)

    def get_poll(self, question_obj=None, poll_pk=None):
        if question_obj:
            self.set_poll(question_obj=question_obj)
        elif poll_pk:
            self.set_poll(poll_pk=poll_pk)
        return self.poll


class QuestionProperties:
    question = None
    question_set = None

    def set_question(self, question_pk):
        self.question = get_object_or_404(Question, pk=question_pk)

    def get_question(self, question_pk=None):
        if question_pk:
            self.set_question(question_pk)
        return self.question

    def set_question_set(self, poll_obj):
        self.question_set = Question.objects.filter(poll=poll_obj).select_related()

    def get_question_set_count(self):
        if self.question_set:
            return len(self.question_set)
        else:
            return None


class ChoiceSetProperties:
    choice_set = None

    def set_choice_set(self, question_obj):
        self.choice_set = Choice.objects.filter(question=question_obj).select_related()

    def get_choice_set(self, question_obj=None):
        if question_obj:
            self.set_choice_set(question_obj)
        return self.choice_set


class ModelProperties(PollProperties,
                      QuestionProperties,
                      ChoiceSetProperties,
                      AnonUserManager):
    question_choice_answer_set = None

    def set_question_choice_answer_set(self, poll, user):
        queryset = Answer.objects.filter(poll=poll, user=user)
        prefetch = Prefetch('answers', queryset=queryset)
        self.question_choice_answer_set = Question.objects.filter(
            poll=poll).prefetch_related('choices', prefetch)

    def get_next_question_or_none(self, poll=None, user=None):
        if not self.question_choice_answer_set:
            self.set_question_choice_answer_set(poll, user)

        for q in self.question_choice_answer_set:
            if not q.answers.all():
                return q
        return None

    def get_choice_set(self, question_obj):
        if self.question_choice_answer_set:
            for question in self.question_choice_answer_set:
                if question == question_obj:
                    return question.choice_set.all()
        else:
            return super().get_choice_set(question_obj)

    def get_result_dict(self):
        results = {}
        for question in self.question_choice_answer_set:
            choices = [choice for choice in question.choices.all()]
            answers = [answer for answer in question.answers.all()]
            results[question.title] = {'question': question,
                                       'choices': choices,
                                       'answers': answers}
        return results

    def get_question_set_count(self):
        if self.question_choice_answer_set:
            return len(self.question_choice_answer_set)
        else:
            return super().get_question_set_count()




class QuestionViewMixin(FormView, ModelProperties):
    template_name = 'polls/question_page.html'

    def dispatch(self, request, *args, **kwargs):

        if not self.question:
            self.set_question(question_pk=self.kwargs['pk'])

        if not self.choice_set:
            self.set_choice_set(self.question)

        if not self.anon_user_obj:
            self.anon_user_obj = self.get_anon_user_object(request)

        if not self.poll:
            self.set_poll(question_obj=self.question)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.question
        return context

    def get_form_class(self):

        if self.question.type == 'WA':
            form = WritenAnswerForm
        elif self.question.type == 'OA':
            form = OneAnswerForm
        elif self.question.type == 'MA':
            form = MultipleAnswerForm
        else:
            return super().get_form_class()

        return form

    def get_form_kwargs(self):

        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }
        if self.question.type != 'WA':
            if self.question.type == 'OA':
                kwargs['queryset'] = self.choice_set
            elif self.question.type == 'MA':
                kwargs['question'] = self.question

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        if self.question.type == 'MA':
            answers = dict(self.request.POST)
            for choice in answers['choices']:
                self.save_answer_obj(choice)
        else:
            self.save_choice_form(form)
        return super().form_valid(form)

    def save_answer_obj(self, choice):
        answer = Answer.objects.create(
            user=self.anon_user_obj,
            question=self.question,
            choice=Choice.objects.get(pk=choice),
            poll=self.poll,
        )
        answer.save()

    def save_choice_form(self, form):
        form = form.save(commit=False)
        form.user_id = self.anon_user_obj.pk
        form.question_id = self.question.pk
        form.poll_id = self.poll.pk
        form.save()
