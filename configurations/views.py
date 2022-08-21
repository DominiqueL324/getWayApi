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
from gateway.settings import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.

class InterventionApi(APIView):

    token_param = openapi.Parameter('Authorization', in_=openapi.IN_HEADER ,description="Token for Auth" ,type=openapi.TYPE_STRING)
    pagination_param = openapi.Parameter('paginated', in_=openapi.IN_QUERY ,description="Paginated data or no" ,type=openapi.TYPE_STRING,required=False)
    page_param = openapi.Parameter('page', in_=openapi.IN_QUERY ,description="Pagination page" ,type=openapi.TYPE_INTEGER,required=False)

    @swagger_auto_schema(manual_parameters=[token_param,pagination_param,page_param])
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
        
        final_=[]
        try:
            interventions = requests.get(URLINTERVENTION,params=request.query_params).json()
            return Response(interventions,status=200) 
        except ValueError:
            return JsonResponse({"status":"failure"},status=401) 

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['data'],
            properties={
                'type': openapi.Schema(type=openapi.TYPE_STRING),
                'statut': openapi.Schema(type=openapi.TYPE_INTEGER),
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

        try:
            interventions = requests.post(URLINTERVENTION,data=self.request.data).json() 
            return Response(interventions,status=200) 
        except ValueError:
            return JsonResponse({"status":"failure"},status=401) 

               
class InterventionDetailsAPI(APIView):
    token_param = openapi.Parameter('Authorization', in_=openapi.IN_HEADER ,description="Token for Auth" ,type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[token_param])
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

        url_ = URLINTERVENTION+str(id)
    
        try:
            intervention = requests.get(url_,params=request.query_params).json() 
            return Response(intervention,status=200)    
        except ValueError:
            return JsonResponse({"status":"failure"},status=401) 
            
    #edit rdv
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['data'],
            properties={
                'type': openapi.Schema(type=openapi.TYPE_STRING),
                'statut': openapi.Schema(type=openapi.TYPE_INTEGER),
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

        try:
            interventions = requests.put(URLINTERVENTION+str(id),data=self.request.data).json()
            return Response(interventions,status=401) 
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
            interventions = requests.delete(URLINTERVENTION+str(id)).json()
            return JsonResponse({"status":"done"},status=200)
        except ValueError:
            return JsonResponse({"status":"failure"},status=401)


class TypeProprieteApi(APIView):

    token_param = openapi.Parameter('Authorization', in_=openapi.IN_HEADER ,description="Token for Auth" ,type=openapi.TYPE_STRING)
    pagination_param = openapi.Parameter('paginated', in_=openapi.IN_QUERY ,description="Paginated data or not" ,type=openapi.TYPE_STRING,required=False)
    page_param = openapi.Parameter('page', in_=openapi.IN_QUERY ,description="Pagination page" ,type=openapi.TYPE_INTEGER,required=False)

    @swagger_auto_schema(manual_parameters=[token_param,pagination_param,page_param])
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
        
        final_=[]
        try:
            proprietes = requests.get(URLPROPRIETE,params=request.query_params).json()
            return Response(proprietes,status=200) 
        except ValueError:
            return JsonResponse({"status":"failure"},status=401) 

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['data'],
            properties={
                'type': openapi.Schema(type=openapi.TYPE_STRING),
                'statut': openapi.Schema(type=openapi.TYPE_INTEGER),
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

        try:
            proprietes = requests.post(URLPROPRIETE,data=self.request.data).json() 
            return Response(proprietes,status=200) 
        except ValueError:
            return JsonResponse({"status":"failure"},status=401) 

               
class TypeProprieteDetailsAPI(APIView):
    
    token_param = openapi.Parameter('Authorization', in_=openapi.IN_HEADER ,description="Token for Auth" ,type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param])
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

        url_ = URLPROPRIETE+str(id)
    
        try:
            propriete = requests.get(url_).json() 
            return Response(propriete,status=200)    
        except ValueError:
            return JsonResponse({"status":"failure"},status=401) 
            
    #edit rdv
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['data'],
            properties={
                'type': openapi.Schema(type=openapi.TYPE_STRING),
                'statut': openapi.Schema(type=openapi.TYPE_INTEGER),
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

        try:
            proprietes = requests.put(URLPROPRIETE+str(id),data=self.request.data).json()
            return Response(proprietes,status=401) 
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
            proprietes = requests.delete(URLPROPRIETE+str(id)).json()
            return JsonResponse({"status":"done"},status=200)
        except ValueError:
            return JsonResponse({"status":"failure"},status=401)

