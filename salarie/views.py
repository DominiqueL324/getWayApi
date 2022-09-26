import json
from typing import final
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import  TokenAuthentication
from rest_framework import generics
from rest_framework import mixins 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User, Group
from datetime import date, datetime,time,timedelta
import requests
from rdv.views import controller
from logger.views import checkRole
from gateway.settings import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from logger.tools import envoyerEmail
# Create your views here.
 
class SalarieApi(APIView):

    token_param = openapi.Parameter('Authorization', in_=openapi.IN_HEADER ,description="Token for Auth" ,type=openapi.TYPE_STRING)
    pagination_param = openapi.Parameter('paginated', in_=openapi.IN_QUERY ,description="Paginated data or no" ,type=openapi.TYPE_STRING,required=False)
    page_param = openapi.Parameter('page', in_=openapi.IN_QUERY ,description="Pagination page" ,type=openapi.TYPE_INTEGER,required=False)
    page_client = openapi.Parameter('client', in_=openapi.IN_QUERY ,description="client" ,type=openapi.TYPE_INTEGER,required=False)

    @swagger_auto_schema(manual_parameters=[token_param,pagination_param,page_param,page_client])
    def get(self,request):

        try:
            token = self.request.headers.__dict__['_store']['authorization'][1].split(' ')[1]
        except KeyError:
            return JsonResponse({"status":"not_logged"},status=401)

        logged = controller(token)
        test = isinstance(logged, list)
        if not test:
        #if "id" not in logged.keys():
            return JsonResponse({"status":"not_logged"},status=401)
        
        #controle des roles 
        role = checkRole(token)
        if role == -1:
            return JsonResponse({"status":"No roles"},status=401) 

        if role['user']['group'] != "Administrateur" and role['user']['group'] != "Agent constat" and role['user']['group'] != "Agent secteur" and  role['user']['group'] != "Client pro":
            return JsonResponse({"status":"insufficient privileges"},status=401)
        
        final_=[]
        try:
            salaries = requests.get(URLSALARIE,params=request.query_params,headers={"Authorization":"Bearer "+token}).json()
            return Response(salaries,status=200) 
        except ValueError:
            return JsonResponse({"status":"failure"},status=401) 

    
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['data'],
            properties={
                'nom': openapi.Schema(type=openapi.TYPE_STRING),
                'prenom': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'login': openapi.Schema(type=openapi.TYPE_STRING),
                'mdp': openapi.Schema(type=openapi.TYPE_STRING),
                'fonction': openapi.Schema(type=openapi.TYPE_STRING),
                'mobile':openapi.Schema(type=openapi.TYPE_STRING),
                'titre':openapi.Schema(type=openapi.TYPE_STRING),
                'agent':openapi.Schema(type=openapi.TYPE_INTEGER),
                'telephone':openapi.Schema(type=openapi.TYPE_STRING),
                'client':openapi.Schema(type=openapi.TYPE_INTEGER),
            },
         ),
        manual_parameters=[token_param])
    def post(self,request):

        try:
            token = self.request.headers.__dict__['_store']['authorization'][1].split(' ')[1]
        except KeyError:
            return JsonResponse({"status":"not_logged"},status=401)

        logged = controller(token)
        test = isinstance(logged, list)
        if not test:
        #if "id" not in logged.keys():
            return JsonResponse({"status":"not_logged"},status=401)

        #controle des roles 
        role = checkRole(token)
        if role == -1:
            return JsonResponse({"status":"No roles"},status=401) 

        if role['user']['group'] != "Administrateur" and role['user']['group'] != "Agent constat" and role['user']['group'] != "Agent secteur" and  role['user']['group'] != "Client pro":
            return JsonResponse({"status":"insufficient privileges"},status=401)

        try:
            salaries = requests.post(URLSALARIE,headers={"Authorization":"Bearer "+token},data=self.request.data).json() 
            return Response(salaries,status=200) 
        except ValueError:
            return JsonResponse({"status":"failure"},status=401) 

               
class SalarieDetailsAPI(APIView):
    token_param = openapi.Parameter('Authorization', in_=openapi.IN_HEADER ,description="Token for Auth" ,type=openapi.TYPE_STRING)
    page_client = openapi.Parameter('client', in_=openapi.IN_QUERY ,description="client" ,type=openapi.TYPE_INTEGER,required=False)
   
    @swagger_auto_schema(manual_parameters=[token_param,page_client])
    def get(self,request,id):

        try:
            token = self.request.headers.__dict__['_store']['authorization'][1].split(' ')[1]
        except KeyError:
            return JsonResponse({"status":"not_logged"},status=401)

        logged = controller(token)
        test = isinstance(logged, list)
        if not test:
        #if "id" not in logged.keys():
            return JsonResponse({"status":"not_logged"},status=401)

        #controle des roles 
        role = checkRole(token)
        if role == -1:
            return JsonResponse({"status":"No roles"},status=401) 

        if role['user']['group'] != "Administrateur" and role['user']['group'] != "Agent constat" and role['user']['group'] != "Agent secteur" and  role['user']['group'] != "Client pro":
            if role['user']['group'] == "Salarie" and int(role['id'])==int(id):
                url_ = URLSALARIE+str(id)
            else:
                return JsonResponse({"status":"insufficient privileges"},status=401)
        else:
            url_ = URLSALARIE+str(id)

        url_ = URLSALARIE+str(id)
    
        try:
            salarie = requests.get(url_,headers={"Authorization":"Bearer "+token}).json() 
            return Response(salarie,status=200)    
        except ValueError:
            return JsonResponse({"status":"failure"},status=401) 
            
    #edit rdv
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['data'],
            properties={
                'nom': openapi.Schema(type=openapi.TYPE_STRING),
                'prenom': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'login': openapi.Schema(type=openapi.TYPE_STRING),
                'mdp': openapi.Schema(type=openapi.TYPE_STRING),
                'fonction': openapi.Schema(type=openapi.TYPE_STRING),
                'mobile':openapi.Schema(type=openapi.TYPE_STRING),
                'titre':openapi.Schema(type=openapi.TYPE_STRING),
                'agent':openapi.Schema(type=openapi.TYPE_INTEGER),
                'telephone':openapi.Schema(type=openapi.TYPE_STRING),
                'client':openapi.Schema(type=openapi.TYPE_INTEGER),
                'is_active':openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
         ),
        manual_parameters=[token_param])
    def put(self,request,id):
        try:
            token = self.request.headers.__dict__['_store']['authorization'][1].split(' ')[1]
        except KeyError:
            return JsonResponse({"status":"not_logged"},status=401)

        logged = controller(token)
        test = isinstance(logged, list)
        if not test:
        #if "id" not in logged.keys():
            return JsonResponse({"status":"not_logged"},status=401)

        #controle des roles 
        role = checkRole(token)
        if role['user']['group'] != "Administrateur" and role['user']['group'] != "Agent constat" and role['user']['group'] != "Agent secteur" and  role['user']['group'] != "Client pro":
            if role['user']['group'] == "Salarie" and int(role['id'])==int(id):
                url_ = URLSALARIE+str(id)
            else:
                return JsonResponse({"status":"insufficient privileges"},status=401)
        else:
            url_ = URLSALARIE+str(id)

        url_ = URLSALARIE+str(id) 

        try:
            salaries = requests.put(url_,headers={"Authorization":"Bearer "+token},data=self.request.data).json()
            contenu = "Modification(s) sur votre espace personnel, connectez vous afin d'en prendre connaissance."
            envoyerEmail("Création de compte",contenu,[salaries[0]['user']['email']],contenu)
            return Response(salaries,status=200) 
        except ValueError:
            return JsonResponse({"status":"failure"},status=401) 
           
    @swagger_auto_schema(manual_parameters=[token_param])
    def delete(self,request,id):
        try:
            token = self.request.headers.__dict__['_store']['authorization'][1].split(' ')[1]
        except KeyError:
            return JsonResponse({"status":"not_logged"},status=401)

        logged = controller(token)
        test = isinstance(logged, list)
        if not test:
        #if "id" not in logged.keys():
            return JsonResponse({"status":"not_logged"},status=401)

        try:
            salaries = requests.delete(URLSALARIE+str(id),headers={"Authorization":"Bearer "+token}).json()
            return JsonResponse({"status":"done"},status=200)
        except ValueError:
            return JsonResponse({"status":"failure"},status=401)


         
            


