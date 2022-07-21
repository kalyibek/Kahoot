from django.http import HttpResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *
from .models import *
from users.views import User


class QuizesList(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']
    filterset_fields = ['groups']


class QuizRetrieve(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuestionsList(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionRetrieve(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class AnswersList(generics.ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class CheckAnswers(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = User.objects.get(pk=request.user.pk)
        question = Question.objects.get(pk=pk)
        data = json.loads(request.body)
        if data['submit']:
            user.passed_tests_number += 1
            user.save()
        if question.get_correct_answer().text == data['answer']:
            fact_time = int(data['time'])
            if fact_time == 1:
                result = 100 - (100 / question.time * fact_time) + (100 / question.time)
            else:
                result = 100 - (100 / question.time * fact_time)
            return HttpResponse(f"Got json data {result}")

    def set_rating(self):
        pass


