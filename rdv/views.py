from http import client
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
from gateway.settings import *
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from logger.tools import envoyerEmail
# Create your views here.

def controller(token):
    rdvs = requests.get(URLMANAGER+token,headers={"Authorization":"Bearer "+token}).json()
    return rdvs

def checkRole(token):
    try:
        user = requests.get("http://127.0.0.1:8050/manager_app/viewset/role/?token="+token,headers={"Authorization":"Bearer "+token}).json()[0]
    except KeyError:
        return -1
    return user

class RdvApi(APIView):

    token_param = openapi.Parameter('Authorization', in_=openapi.IN_HEADER ,description="Token for Auth" ,type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param])
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
        
        role = checkRole(token)
        if role == -1:
            return JsonResponse({"status":"No roles"},status=401) 

        if role['user']['group'] != "Administrateur" and role['user']['group'] != "Agent constat" and role['user']['group'] != "Agent secteur" and role['user']['group'] != "Client pro" and role['user']['group'] != "Client particulier":
            return JsonResponse({"status":"insufficient privileges"},status=401)

        url_ = URLRDV

        if role['user']['group'] == "Client particulier" or role['user']['group'] == "Client pro":
            url_ = url_+"?user="+str(role['id'])
        
        if role['user']['group'] == "Agent secteur":
            url_ = url_+"?agent="+str(role['id'])

        finaly_ ={}
        """if(request.GET.get("value",None) is not None):
            url_ = URLUSERS
            val_ = request.GET.get("value",None)
            users = requests.get(url_,params=request.query_params,headers={"Authorization":"Bearer "+token}).json()
            for user in users:
                rdvs = requests.get(URLRDV,params={"user":user.client}).json()
                for rdv in rdvs:
                   finaly_.append(rdv)
            return Response(finaly_,status=status.HTTP_200_OK)"""

        final_ = []
        rdvs = requests.get(url_,params=request.query_params)
        finaly_ ={}
        for rdv in rdvs.json()['results']:
            try:
                rdv['client'] = requests.get(URLCLIENT+str(rdv['client']),headers={"Authorization":"Bearer "+token}).json()[0]
                if rdv['agent'] is not None:
                    rdv['agent'] = requests.get(URLAGENT+str(rdv['agent']),headers={"Authorization":"Bearer "+token}).json()[0]
                if rdv['passeur'] is not None:
                    rdv['passeur'] = requests.get(URLSALARIE+str(rdv['passeur']),headers={"Authorization":"Bearer "+token}).json()[0]
            except ValueError:
                return JsonResponse({"status":"failure"}) 
            final_.append(rdv)
        finaly_['count'] = rdvs.json()['count']
        finaly_['next'] = rdvs.json()['next']
        finaly_['previous'] = rdvs.json()['previous']
        finaly_['results'] = final_
        return Response(finaly_,status=status.HTTP_200_OK)


    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['data'],
            properties={
                'nom_bailleur': openapi.Schema(type=openapi.TYPE_STRING),
                'prenom_bailleur': openapi.Schema(type=openapi.TYPE_STRING),
                'email_bailleur': openapi.Schema(type=openapi.TYPE_STRING),
                'reference_bailleur': openapi.Schema(type=openapi.TYPE_STRING),
                'nom_locataire': openapi.Schema(type=openapi.TYPE_STRING),
                'prenom_locataire': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'email_locataire': openapi.Schema(type=openapi.TYPE_STRING),
                'telephone_locataire': openapi.Schema(type=openapi.TYPE_STRING),
                'surface_propriete' : openapi.Schema(type=openapi.TYPE_STRING),
                'numero_propriete' : openapi.Schema(type=openapi.TYPE_STRING),
                'numero_parking_propriete' : openapi.Schema(type=openapi.TYPE_STRING),
                'adresse_propriete' : openapi.Schema(type=openapi.TYPE_STRING),
                'code_postal_propriete' : openapi.Schema(type=openapi.TYPE_STRING),
                'ville_propriete' : openapi.Schema(type=openapi.TYPE_STRING),
                'adresse_complementaire_propriete' : openapi.Schema(type=openapi.TYPE_STRING),
                'numero_cave_propriete' : openapi.Schema(type=openapi.TYPE_STRING),
                'numero_sol_propriete' : openapi.Schema(type=openapi.TYPE_INTEGER),
                'ref_lot' : openapi.Schema(type=openapi.TYPE_STRING),
                'ref_edl' : openapi.Schema(type=openapi.TYPE_STRING),
                'intervention' : openapi.Schema(type=openapi.TYPE_INTEGER),
                'client' : openapi.Schema(type=openapi.TYPE_INTEGER),
                'statut' : openapi.Schema(type=openapi.TYPE_INTEGER),
                'date' : openapi.Schema(type=openapi.TYPE_STRING),
                'passeur' : openapi.Schema(type=openapi.TYPE_INTEGER),
                'agent': openapi.Schema(type=openapi.TYPE_INTEGER),
                'longitude':openapi.Schema(type=openapi.TYPE_STRING),
                'latitude':openapi.Schema(type=openapi.TYPE_STRING),
                'type_propriete': openapi.Schema(type=openapi.TYPE_INTEGER),
                'type': openapi.Schema(type=openapi.TYPE_STRING),
                'consignes_part': openapi.Schema(type=openapi.TYPE_STRING),
                'list_documents': openapi.Schema(type=openapi.TYPE_STRING),
                'info_diverses': openapi.Schema(type=openapi.TYPE_STRING),
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

        #contrôle des roles
        role = checkRole(token)
        if role == -1:
            return JsonResponse({"status":"No roles"},status=401) 

        if role['user']['group'] != "Administrateur" and role['user']['group'] != "Agent constat" and role['user']['group'] != "Agent secteur" and role['user']['group'] != "Client pro" and role['user']['group'] != "Client particulier":
            return JsonResponse({"status":"insufficient privileges"},status=401)

        final_=[]
        try:
            rdvs = requests.post(URLRDV,data=self.request.data).json()[0]
        except KeyError:
            return JsonResponse({"status":"failure to post data"}) 

        rdvs = requests.get(URLRDV+str(rdvs['id']))
        for rdv in rdvs.json():
            try:
                rdv['client'] = requests.get(URLCLIENT+str(rdv['client']),headers={"Authorization":"Bearer "+token}).json()[0]
                rdv['agent'] = requests.get(URLAGENT+str(rdv['agent']),headers={"Authorization":"Bearer "+token}).json()[0]
                rdv['passeur'] = requests.get(URLSALARIE+str(rdv['passeur']),headers={"Authorization":"Bearer "+token}).json()[0]
            except KeyError:
                return JsonResponse({"status":"failure to get response"})
            contenu = "Votre commande est enregistrée."
            envoyerEmail("Création de compte",contenu,[rdv['client']['user']['email']],contenu) 
            final_.append(rdv)
        return Response(final_,status=status.HTTP_201_CREATED)

               
class RdvApiDetails(APIView):
    
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
        
        role = checkRole(token)
        if role == -1:
            return JsonResponse({"status":"No roles"},status=401) 

        if role['user']['group'] != "Administrateur" and role['user']['group'] != "Agent constat" and role['user']['group'] != "Agent secteur" and role['user']['group'] != "Client pro" and role['user']['group'] != "Client particulier":
            return JsonResponse({"status":"insufficient privileges"},status=401)

        url_ = URLRDV

        final_ = []
        url_ = URLRDV+str(id)
        rdvs = requests.get(url_)

        try:
            for rdv in rdvs.json():
                rdv['client'] = requests.get(URLCLIENT+str(rdv['client']),headers={"Authorization":"Bearer "+token}).json()[0]
                rdv['agent'] = requests.get(URLAGENT+str(rdv['agent']),headers={"Authorization":"Bearer "+token}).json()[0]
                rdv['passeur'] = requests.get(URLSALARIE+str(rdv['passeur']),headers={"Authorization":"Bearer "+token}).json()[0]
                final_.append(rdv)
        except ValueError:
                return JsonResponse({"status":"failure"},status=401) 
            
        return Response(final_,status=status.HTTP_200_OK)

    #edit rdv

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['data'],
            properties={
                'nom_bailleur': openapi.Schema(type=openapi.TYPE_STRING),
                'prenom_bailleur': openapi.Schema(type=openapi.TYPE_STRING),
                'email_bailleur': openapi.Schema(type=openapi.TYPE_STRING),
                'reference_bailleur': openapi.Schema(type=openapi.TYPE_STRING),
                'nom_locataire': openapi.Schema(type=openapi.TYPE_STRING),
                'prenom_locataire': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                'email_locataire': openapi.Schema(type=openapi.TYPE_STRING),
                'telephone_locataire': openapi.Schema(type=openapi.TYPE_STRING),
                'surface_propriete' : openapi.Schema(type=openapi.TYPE_STRING),
                'numero_propriete' : openapi.Schema(type=openapi.TYPE_STRING),
                'numero_parking_propriete' : openapi.Schema(type=openapi.TYPE_STRING),
                'adresse_propriete' : openapi.Schema(type=openapi.TYPE_STRING),
                'code_postal_propriete' : openapi.Schema(type=openapi.TYPE_STRING),
                'ville_propriete' : openapi.Schema(type=openapi.TYPE_STRING),
                'adresse_complementaire_propriete' : openapi.Schema(type=openapi.TYPE_STRING),
                'numero_cave_propriete' : openapi.Schema(type=openapi.TYPE_STRING),
                'numero_sol_propriete' : openapi.Schema(type=openapi.TYPE_INTEGER),
                'ref_lot' : openapi.Schema(type=openapi.TYPE_STRING),
                'ref_edl' : openapi.Schema(type=openapi.TYPE_STRING),
                'intervention' : openapi.Schema(type=openapi.TYPE_INTEGER),
                'client' : openapi.Schema(type=openapi.TYPE_INTEGER),
                'date' : openapi.Schema(type=openapi.TYPE_STRING),
                'statut' : openapi.Schema(type=openapi.TYPE_INTEGER),
                'passeur' : openapi.Schema(type=openapi.TYPE_INTEGER),
                'agent': openapi.Schema(type=openapi.TYPE_INTEGER),
                'longitude':openapi.Schema(type=openapi.TYPE_STRING),
                'latitude':openapi.Schema(type=openapi.TYPE_STRING),
                'type_propriete': openapi.Schema(type=openapi.TYPE_INTEGER),
                'type': openapi.Schema(type=openapi.TYPE_STRING),
                'consignes_part': openapi.Schema(type=openapi.TYPE_STRING),
                'list_documents': openapi.Schema(type=openapi.TYPE_STRING),
                'info_diverses': openapi.Schema(type=openapi.TYPE_STRING),
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

        role = checkRole(token)
        if role == -1:
            return JsonResponse({"status":"No roles"},status=401) 

        if role['user']['group'] != "Administrateur" and role['user']['group'] != "Agent constat" and role['user']['group'] != "Agent secteur" and role['user']['group'] != "Client pro" and role['user']['group'] != "Client particulier":
            return JsonResponse({"status":"insufficient privileges"},status=401)

        url_ = URLRDV

        final_=[]
        try:
            rdvs = requests.put(URLRDV+str(id),data=self.request.data).json()[0]
        except ValueError:
            return JsonResponse({"status":"failure to update data"},status=401) 

        rdvs = requests.get(URLRDV+str(rdvs['id']))
        try:
            for rdv in rdvs.json():
                
                rdv['client'] = requests.get(URLCLIENT+str(rdv['client']),headers={"Authorization":"Bearer "+token}).json()[0]
                rdv['agent'] = requests.get(URLAGENT+str(rdv['agent']),headers={"Authorization":"Bearer "+token}).json()[0]
                rdv['passeur'] = requests.get(URLSALARIE+str(rdv['passeur']),headers={"Authorization":"Bearer "+token}).json()[0]
                final_.append(rdv)
        except ValueError:
                return JsonResponse({"status":"failure to get data"},status=401) 
           
        return Response(final_,status=status.HTTP_201_CREATED)

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

        role = checkRole(token)
        if role == -1:
            return JsonResponse({"status":"No roles"},status=401) 

        if role['user']['group'] != "Administrateur" and role['user']['group'] != "Agent constat" and role['user']['group'] != "Agent secteur" and role['user']['group'] != "Client":
            return JsonResponse({"status":"insufficient privileges"},status=401)

        url_ = URLRDV

        try:
            rdvs = requests.delete(URLRDV+str(id)).json()
            return JsonResponse({"status":"done"},status=200)
        except ValueError:
            return JsonResponse({"status":"failure"},status=401)


