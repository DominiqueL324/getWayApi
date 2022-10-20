from django.urls import path
from rest_framework.views import APIView
from . import views
from .views import LoginApi,checkExistingMails, RefreshToken, GetPassword
from rest_framework.authtoken import views


urlpatterns = [
    path('login/', LoginApi.as_view()),
    path('refresh/token/', RefreshToken.as_view()),
    path('logout/', LoginApi.as_view()),
    path('checker/', checkExistingMails.as_view()),
    path('backup/password/', GetPassword.as_view()),
]