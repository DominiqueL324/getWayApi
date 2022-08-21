from django.urls import path
from rest_framework.views import APIView
from . import views
from .views import RdvApi,RdvApiDetails
from rest_framework.authtoken import views


urlpatterns = [
    path('rdv/', RdvApi.as_view()),
    path('rdv/<int:id>', RdvApiDetails.as_view()),
]