from django.urls import path
from rest_framework.views import APIView
from . import views
from .views import InterventionApi,InterventionDetailsAPI,TypeProprieteApi,TypeProprieteDetailsAPI
from rest_framework.authtoken import views


urlpatterns = [
    path('intervention/', InterventionApi.as_view()),
    path('intervention/<int:id>', InterventionDetailsAPI.as_view()),
    path('propriete/', TypeProprieteApi.as_view()),
    path('propriete/<int:id>', TypeProprieteDetailsAPI.as_view()),
]