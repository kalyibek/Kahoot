from rest_framework import viewsets, mixins
from rest_framework import filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *
from .models import *


class QuizesViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.RetrieveModelMixin):

    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description']


class QuestionsViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       mixins.RetrieveModelMixin):

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)


class QuestionResultViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin):

    serializer_class = QuestionResultSerializer
    queryset = QuestionResult.objects.all()
    permission_classes = (IsAuthenticated,)


class QuestionResultCreateViewSet(viewsets.GenericViewSet,
                                  mixins.CreateModelMixin):

    serializer_class = AnswerCheckSerializer
    queryset = QuestionResult.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        QuestionResult.calculate_score(**serializer.validated_data)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
