from rest_framework import serializers
from .models import *


class AnswerCheckSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    question_id = serializers.IntegerField()
    quiz_id = serializers.IntegerField()
    answer = serializers.CharField(max_length=255)
    fact_time = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class QuizSubmitSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    quiz_id = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class QuestionResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionResult
        fields = '__all__'


class QuizResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuizResult
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    answer_set = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'quiz', 'time', 'answer_set']


class QuizSerializer(serializers.ModelSerializer):

    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'description', 'created', 'question_set']
