from django.urls import path
from rest_framework.views import APIView
from . import views
from .views import ClientApi,ClientDetailsAPI
from rest_framework.authtoken import views


urlpatterns = [
    path('client/', ClientApi.as_view()),
    path('client/<int:id>', ClientDetailsAPI.as_view()),
]