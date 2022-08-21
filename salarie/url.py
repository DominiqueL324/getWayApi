from django.urls import path
from rest_framework.views import APIView
from . import views
from .views import SalarieApi,SalarieDetailsAPI
from rest_framework.authtoken import views


urlpatterns = [
    path('salarie/', SalarieApi.as_view()),
    path('salarie/<int:id>', SalarieDetailsAPI.as_view()),
]