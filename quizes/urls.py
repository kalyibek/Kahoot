from django.urls import path, include
from . import views

urlpatterns = [
    path('quizes/', views.QuizesList.as_view()),
    path('quizes/<int:pk>/', views.QuizRetrieve.as_view()),
    path('questions/<int:pk>/', views.CheckAnswers.as_view()),
]
