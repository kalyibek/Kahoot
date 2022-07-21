from rest_framework import serializers
from .models import *


class AnswerSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Answer.objects.create(**validated_data)

    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):

    answer_set = AnswerSerializer(many=True)

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    class Meta:
        model = Question
        fields = ['id', 'text', 'quiz', 'time', 'answer_set']


class QuizSerializer(serializers.ModelSerializer):

    question_set = QuestionSerializer(many=True)

    def create(self, validated_data):
        return Quiz.objects.create(**validated_data)

    class Meta:
        model = Quiz
        fields = ['id', 'name', 'description', 'created', 'groups', 'question_set']
