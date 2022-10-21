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

class ClientApi(APIView):

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
        
        #controle des roles 
        role = checkRole(token)
        if role == -1:
            return JsonResponse({"status":"No roles"},status=401) 

        if role['user']['group'] != "Administrateur" and role['user']['group'] != "Agent secteur" and role['user']['group'] != "Agent constat" and role['user']['group'] != "Audit planneur":
            return JsonResponse({"status":"insufficient privileges"},status=401)

        url_= URLCLIENT
        if role ['user']['group']  == "Agent secteur" or role['user']['group'] == "Agent constat" or role['user']['group'] == "Audit planneur":
            url_ = url_+"?token="+token

        final_=[]
        try:
            clients = requests.get(url_,headers={"Authorization":"Bearer "+token},params=self.request.query_params).json()
            return Response(clients,status=200) 
        except ValueError:
            return JsonResponse({"status":"failure"},status=401)


    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['data'],
            properties={
                'nom': openapi.Schema(type=openapi.TYPE_STRING),
                'prenom': openapi.Schema(type=openapi.TYPE_STRING),
                'email_reponsable': openapi.Schema(type=openapi.TYPE_STRING),
                'login': openapi.Schema(type=openapi.TYPE_STRING),
                'mdp': openapi.Schema(type=openapi.TYPE_STRING),
                'code_client': openapi.Schema(type=openapi.TYPE_STRING),
                'adresse':openapi.Schema(type=openapi.TYPE_STRING),
                'telephone':openapi.Schema(type=openapi.TYPE_STRING),
                'type':openapi.Schema(type=openapi.TYPE_STRING),
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

        if role['user']['group'] != "Administrateur" and role['user']['group'] != "Agent secteur" and role['user']['group'] != "Agent constat" and role['user']['group'] != "Audit planneur":
            return JsonResponse({"status":"insufficient privileges"},status=401)

        try:
            clients = requests.post(URLCLIENT,headers={"Authorization":"Bearer "+token},data=self.request.data).json() 
            return Response(clients,status=200) 
        except ValueError:
            return JsonResponse({"status":"failure"},status=401) 

               
class ClientDetailsAPI(APIView):
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
        
        #controle des roles 
        role = checkRole(token)
        if role == -1:
            return JsonResponse({"status":"No roles"},status=401) 

        if role['user']['group'] != "Administrateur" and role['user']['group'] != "Agent secteur" and role['user']['group'] != "Agent constat" and role['user']['group'] != "Audit planneur":
            if (role['user']['group'] == "Client pro" or role['user']['group'] == "Client particulier") and int(role['id'])==int(id):
                url_ = URLCLIENT+str(id)
            else:
                return JsonResponse({"status":"insufficient privileges"},status=401)
        else:
            url_ = URLCLIENT+str(id)
        
        try:
            client = requests.get(url_,headers={"Authorization":"Bearer "+token}).json() 
            return Response(client,status=200)    
        except ValueError:
            return JsonResponse({"status":"failure"},status=401) 
            
    #edit client
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['data'],
            properties={
                'nom': openapi.Schema(type=openapi.TYPE_STRING),
                'prenom': openapi.Schema(type=openapi.TYPE_STRING),
                'email_reponsable': openapi.Schema(type=openapi.TYPE_STRING),
                'login': openapi.Schema(type=openapi.TYPE_STRING),
                'mdp': openapi.Schema(type=openapi.TYPE_STRING),
                'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'type':openapi.Schema(type=openapi.TYPE_INTEGER),
                'adresse': openapi.Schema(type=openapi.TYPE_STRING),
                'code_client': openapi.Schema(type=openapi.TYPE_STRING),
                'nom_complet_comptable' : openapi.Schema(type=openapi.TYPE_STRING),
                'email_envoi_facture' : openapi.Schema(type=openapi.TYPE_STRING),
                'telephone_comptable' : openapi.Schema(type=openapi.TYPE_STRING),
                'mobile_comptable' : openapi.Schema(type=openapi.TYPE_STRING),
                'nom_complet_contact' : openapi.Schema(type=openapi.TYPE_STRING),
                'email_service_gestion' : openapi.Schema(type=openapi.TYPE_STRING),
                'telephone_service_gestion' : openapi.Schema(type=openapi.TYPE_STRING),
                'mobile_service_gestion' : openapi.Schema(type=openapi.TYPE_STRING),
                'agent_rattache' : openapi.Schema(type=openapi.TYPE_INTEGER),
                'agence_secteur_rattachement' : openapi.Schema(type=openapi.TYPE_STRING),
                'nom_concessionnaire' : openapi.Schema(type=openapi.TYPE_STRING),
                'numero_proposition_prestation' : openapi.Schema(type=openapi.TYPE_STRING),
                'as_client' : openapi.Schema(type=openapi.TYPE_STRING),
                'origine_client' : openapi.Schema(type=openapi.TYPE_STRING),
                'suivie_technique_client' : openapi.Schema(type=openapi.TYPE_STRING),
                'statut_client': openapi.Schema(type=openapi.TYPE_INTEGER),
                'titre':openapi.Schema(type=openapi.TYPE_STRING),
                'fonction':openapi.Schema(type=openapi.TYPE_STRING),
                'societe' : openapi.Schema(type=openapi.TYPE_STRING),
                'ref_societe' : openapi.Schema(type=openapi.TYPE_STRING),
                'email_agence' : openapi.Schema(type=openapi.TYPE_STRING),
                'siret' : openapi.Schema(type=openapi.TYPE_STRING),
                'tva_intercommunautaire' : openapi.Schema(type=openapi.TYPE_STRING),
                'complement_adresse' : openapi.Schema(type=openapi.TYPE_STRING),
                'code_postal' : openapi.Schema(type=openapi.TYPE_STRING),
                'ville' : openapi.Schema(type=openapi.TYPE_STRING),
                'telephone' : openapi.Schema(type=openapi.TYPE_STRING),
                'mobile' : openapi.Schema(type=openapi.TYPE_STRING),
                'telephone_agence' : openapi.Schema(type=openapi.TYPE_STRING),
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
        if role['user']['group'] != "Administrateur" and role['user']['group'] != "Agent secteur" and role['user']['group'] != "Agent constat" and role['user']['group'] != "Audit planneur" and role['user']['group'] == "Client particulier" and role['user']['group'] == "Client pro":
            if role['user']['group'] == "Client pro" and int(role['id'])==int(id):
                url_ = URLCLIENT+str(id)
            elif role['user']['group'] == "Client particulier" and int(role['id'])==int(id):
                url_ = URLCLIENT+str(id)
            else:
                return JsonResponse({"status":"insufficient privileges"},status=401)
        else:
            url_ = URLCLIENT+str(id)

        try:
            clients = requests.put(url_,headers={"Authorization":"Bearer "+token},data=self.request.data).json()
            contenu = "Modification(s) sur votre espace personnel, connectez vous afin d'en prendre connaissance."
            clients[0]['email'] = envoyerEmail("Création de compte",contenu,[clients[0]['user']['email']],contenu)
            clients[0]['email_send'] = clients[0]['user']['email']
            
            return Response(clients,status=200) 
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

        #controle des roles 
        role = checkRole(token)
        
        if role['user']['group'] != "Administrateur" and role['user']['group'] != "Agent secteur" and role['user']['group'] != "Client pro" and role['user']['group'] != "Client particulier":
            if role['user']['group'] == "Client pro" and int(role['id'])==int(id):
                url_ = URLCLIENT+str(id)
            elif role['user']['group'] == "Client particulier" and int(role['id'])==int(id):
                url_ = URLCLIENT+str(id)
            else:
                return JsonResponse({"status":"insufficient privileges"},status=401)
        else:
            url_ = URLCLIENT+str(id)

        try:
            clients = requests.delete(url_,headers={"Authorization":"Bearer "+token}).json()
            return JsonResponse({"status":"done"},status=200)
        except ValueError:
            return JsonResponse({"status":"failure"},status=401)


         
            


