from django.urls import path
from . import views

urlpatterns = [
    path('quizes/', views.QuizesViewSet.as_view({'get': 'list'})),
    path('quizes/<int:pk>/', views.QuizesViewSet.as_view({'get': 'retrieve'})),

    path('questions/', views.QuestionsViewSet.as_view({'get': 'list'})),
    path('questions/<int:pk>', views.QuestionsViewSet.as_view({'get': 'retrieve'})),

    path('question_result/', views.QuestionResultViewSet.as_view({'get': 'list'})),
    path('question_result/<int:pk>/', views.QuestionResultViewSet.as_view({'get': 'retrieve'})),
    path('question_result/<int:pk>/submit/', views.QuestionResultCreateViewSet.as_view({'post': 'create'})),


    path('quiz_result/', views.QuizResultViewSet.as_view({'get': 'list'})),
    path('quiz_result/<int:pk>', views.QuizResultViewSet.as_view({'get': 'retrieve'})),
    path('quiz_result/<int:pk>/submit/', views.QuizResultCreateViewSet.as_view({'post': 'create'})),
]
