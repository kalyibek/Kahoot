from django.db.models import Sum
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


class QuizResultsList(generics.ListAPIView):
    queryset = QuizResult.objects.all()
    serializer_class = QuizResultSerializer


class QuestionResultsList(generics.ListAPIView):
    queryset = QuestionResult.objects.all()
    serializer_class = QuestionResultSerializer


class CheckAnswers(APIView):

    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk):
        data = json.loads(request.body)
        user = User.objects.get(pk=request.user.pk)
        group = Group.objects.get(pk=user.groups.pk)
        question = Question.objects.get(pk=pk)
        quiz = Quiz.objects.get(pk=data['quiz'])
        result = 0
        if question.get_correct_answer().text == data['answer']:
            fact_time = data['time']
            if fact_time == 1:
                result = 100 - (100 / question.time * fact_time) + (100 / question.time)
            else:
                result = 100 - (100 / question.time * fact_time)
            question_score = QuestionResult.objects.create(score=result, user=user, quiz=quiz, group=group)
            question_score.save()

        if data['submit']:
            question_scores = QuestionResult.objects.filter(user=user, quiz=quiz, group=group)
            final_score = question_scores.aggregate(Sum('score'))['score__sum'] / question_scores.count()
            quiz_score = QuizResult.objects.create(score=final_score, user=user, quiz=quiz, group=group)
            quiz_score.save()
            user.passed_tests_number += 1
            user.save()
            user_scores = QuizResult.objects.filter(user=user)
            user_global_score = user_scores.aggregate(Sum('score'))['score__sum'] / user_scores.count()
            user.final_score = user_global_score
            user.save()

            return HttpResponse(f"Quiz score {final_score}")

        return HttpResponse(f"Question score {result}")
