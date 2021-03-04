from django.db import models
from django.contrib.sessions.models import Session
from django.urls import reverse
from django.conf import settings

from django.core.validators import ValidationError


class AnonUserId(models.Model):
    session = models.OneToOneField(Session, on_delete=models.DO_NOTHING, null=True)
    auth_user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True,
                                     on_delete=models.DO_NOTHING)

    def clean(self):
        super().clean()
        if self.session is None and self.auth_user is None:
            raise ValidationError('Field "session" and "auth_user" are empty! '
                                  'Must be filled at least one of')


class Poll(models.Model):
    title = models.CharField(max_length=256, verbose_name='название')
    description = models.TextField(max_length=4096, verbose_name='описание')
    photo = models.ImageField(upload_to='photos/%y/%m/%d/',
                              verbose_name='фотография', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='изменено')
    end_date = models.DateField(blank=True, verbose_name='дата окончания')
    visible = models.BooleanField(default=False, verbose_name='видимость на сайте')

    def get_absolute_url(self):
        return reverse('view_poll', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'
        ordering = ['id']


class Question(models.Model):
    TYPES = (
        ('OA', 'один ответ'),
        ('MA', 'несколько ответов'),
        ('WA', 'письменный ответ'),
    )

    title = models.CharField(max_length=256, verbose_name='шапка')
    type = models.CharField(max_length=2, choices=TYPES, default='OA',
                            verbose_name='тип вопроса')
    text = models.CharField(max_length=2048, verbose_name='текст вопроса')
    poll = models.ForeignKey(Poll, on_delete=models.DO_NOTHING,
                             verbose_name='опрос', related_name='questions')

    def __str__(self):
        return self.title

    def get_poll_pk(self):
        return Poll.objects.get(pk=self.poll.pk)

    def get_choices_list(self):
        return [(choice.id, choice.text) for choice in self.get_choices()]

    def get_choices(self):
        return Choice.objects.filter(question=self).select_related()

    def get_absolute_url(self):
        return reverse('view_question', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['id']


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 verbose_name='вопрос', related_name='choices')
    text = models.CharField(max_length=2048, verbose_name='текст варианта')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'
        ordering = ['id']


class AnswerManager(models.Manager):

    def create(self, user, poll, question, choice=None, text=None):
        if not choice and not text:
            raise ValidationError('''Field "choice" and "text" are empty! 
            Must be filled at least one of''')
        answer = Answer(user=user,
                        poll=poll,
                        question=question,
                        choice=choice,
                        text=text)
        answer.save()
        return answer


class Answer(models.Model):
    user = models.ForeignKey(AnonUserId, on_delete=models.DO_NOTHING,
                             verbose_name='ID пользователя', null=True,
                             related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE,
                                 verbose_name='вопрос', related_name='answers')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE,
                               verbose_name='вариант ответа', null=True,
                               blank=False, default=None, related_name='answers')
    poll = models.ForeignKey(Poll, on_delete=models.DO_NOTHING,
                             verbose_name='опрос', related_name='answers')

    text = models.CharField(max_length=2048, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='получен')

    objects = AnswerManager()

    def clean(self):
        super().clean()
        if self.choice is None and self.text is None:
            raise ValidationError('Field "choice" and "text" are empty! '
                                  'Must be filled at least one of')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['id']




