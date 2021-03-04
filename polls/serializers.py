from rest_framework import serializers

from .models import Choice, Question, Poll, Answer


class AnswerListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        print('validated_data', validated_data)
        answers = [Answer(**item) for item in validated_data]
        return Answer.objects.bulk_create(answers)


class AnswerSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        print('to_representation', instance)
        return super().to_representation(instance)

    class Meta:
        model = Answer
        fields = ['choice', 'text', 'user', 'question', 'poll']
        list_serializer_class = AnswerListSerializer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'question', 'text']


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    # answers = AnswerSerializer(many=True)
    answers = serializers.SerializerMethodField()
    choices = ChoiceSerializer(many=True, read_only=True)
    poll = serializers.HyperlinkedRelatedField(view_name='poll-detail', read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'title', 'type', 'text', 'poll', 'url', 'choices', 'answers']
        read_only_fields = ['title', 'type', 'text', 'poll', 'url']

    def get_answers(self, obj):
        answers = Answer.objects.filter(question=obj, user=self.context['user_id'])
        if answers:
            answers = AnswerSerializer(answers, many=True).data
            return answers
        else:
            data = Answer(question=obj,
                          poll_id=obj.poll_id,
                          user=self.context['user_id'])
            answers = AnswerSerializer(data, write_only=True).data
            return answers

    def update(self, instance, validated_data):
        print(instance)
        print(validated_data)


class PollSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Poll
        fields = ['pk', 'title', 'description', 'photo', 'updated_at',
                  'end_date', 'questions', 'url']
