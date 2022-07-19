from django.urls import path, include
from .views import TestView, UsersList, UsersRetrieve

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('test/', TestView.as_view()),
    path('profiles/', UsersList.as_view()),
    path('profiles/<int:pk>/', UsersRetrieve.as_view()),
]
