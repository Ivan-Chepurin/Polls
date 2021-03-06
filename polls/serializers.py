from rest_framework import serializers

from .models import Choice, Question, Poll, Answer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id',
                  'question',
                  'text']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'title',
            'text',
            'type',
            'choices',
        ]


class AnswerCreateSerializer(serializers.HyperlinkedModelSerializer):
    question = serializers.SerializerMethodField()
    poll = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_question(self, obj):
        return QuestionSerializer(self.context['question'], read_only=True)

    def get_poll(self, obj):
        poll_id = self.context['question'].poll_id
        return serializers.IntegerField(initial=poll_id, read_only=True)

    def get_user(self, obj):
        user_id = self.context['user_id'].id
        return serializers.IntegerField(initial=user_id, read_only=True)

    class Meta:
        model = Answer
        fields = [
            'choice',
            'text',
            'question',
            'poll',
            'user'
        ]
        read_only_fields = [
            'question',
            'poll',
            'user'
        ]


class AnswerResultList(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = [
            'choice',
            'text',
            'question',
            'poll',
            'user'
        ]


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    answers = AnswerCreateSerializer(read_only=True)
    choices = ChoiceSerializer(many=True, read_only=True)
    poll = serializers.HyperlinkedRelatedField(view_name='poll-detail', read_only=True)

    class Meta:
        model = Question
        fields = [
            'id',
            'title',
            'type',
            'text',
            'poll',
            'url',
            'choices',
            'answers'
        ]
        read_only_fields = [
            'title',
            'type',
            'text',
            'poll',
            'url'
        ]

    # def get_answers(self, obj):
    #     answers = Answer.objects.filter(question=obj, user=self.context['user_id'])
    #     print(answers)
    #     if answers:
    #         print('попал сюда')
    #         answers = AnswerResultList(answers, many=True).data
    #         return answers
    #     else:
    #         answers =
    #         return answers


class PollSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Poll
        fields = [
            'pk',
            'title',
            'description',
            'photo',
            'updated_at',
            'end_date',
            'questions',
            'url'
        ]
