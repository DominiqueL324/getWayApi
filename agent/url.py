from django.urls import path
from rest_framework.views import APIView
from . import views
from .views import AgentApi,AgentDetailsAPI
from rest_framework.authtoken import views


urlpatterns = [
    path('agent/', AgentApi.as_view()),
    path('agent/<int:id>', AgentDetailsAPI.as_view()),
]