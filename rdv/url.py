from django.urls import path
from rest_framework.views import APIView
from . import views
from .views import RdvApi,RdvApiDetails, importRdvApi,commentaireApi,documentAPI,TriRdvApi
from rest_framework.authtoken import views


urlpatterns = [
    path('rdv/', RdvApi.as_view()),
    path('rdv/import/', importRdvApi.as_view()),
    path('rdv/comments/', commentaireApi.as_view()),
    path('rdv/documents/', documentAPI.as_view()),
    path('rdv/tri/', TriRdvApi.as_view()),
    path('rdv/<int:id>', RdvApiDetails.as_view()),
]