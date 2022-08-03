from django.urls import path, include
from .views import UsersList

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
    path('profiles/', UsersList.as_view()),
]
