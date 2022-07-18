from django.urls import path, include
from .views import TestView, UsersList, UsersRetrieve

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('test/', TestView.as_view()),
    path('profiles/', UsersList.as_view()),
    path('profiles/<int:pk>/', UsersRetrieve.as_view()),
]
