from re import S
from django.contrib.auth.models import Permission
from django.shortcuts import render
from rest_framework import response
# from rest_framework.authtoken.models import Token

from rest_framework.authtoken.models import Token
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, serializers

from family.models import user, family, package
from .serializers import *
import string
import random


from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view


chema = openapi.Schema(type=openapi.TYPE_STRING,)
res200 = openapi.Response("returns Authentication token", schema=chema)
res400 = openapi.Response("invalid request", schema=chema)
@swagger_auto_schema(methods=['post'], request_body=UserSerializer, responses={200:res200, 400:res400})
@api_view(('POST',))
@permission_classes((permissions.AllowAny,))
def register_person(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        usr = serializer.save()
        data = {}
        data['token'] = Token.objects.get(user=usr).key
        return Response(data, status=200)
    print(serializer.errors)
    return Response("invalid request",status=400)





chema = openapi.Schema(description="reeturns string which describes status", type=openapi.TYPE_STRING, format=None, enum=None, pattern=None,
properties=None, required=None, items=None,default=None, read_only=None)
res400 = openapi.Response("invalid request", schema=chema)
res401 = openapi.Response("Unauthorized client", schema=chema)
res201 = openapi.Response("created", schema=chema)
@swagger_auto_schema(methods=['post'], request_body=CreateFamilySerializer, responses={400: res400, 401: res401, 201: res201})
@api_view(('POST',))
def create_family(request):
    serializer = CreateFamilySerializer(data=request.data)
    if not serializer.is_valid():
        return Response("invalid request",status=400)

    authentication = False
    parent1 = user.objects.get(username=serializer.data["parents_username"][0])
    if request.user.username == parent1.username:
        authentication = True
    parent2 = None
    if len(serializer.data["parents_username"])==2:
        parent2 = user.objects.get(username=serializer.data["parents_username"][1])
        if request.user.username == parent2.username:
                authentication = True
    if authentication==False:
        return Response("Unauthorized client",status=401)

    if ((len(serializer.data["parents_username"])==1 and len(serializer.data["childs_username"])<1) 
    or (len(serializer.data["parents_username"])<1)
    or (len(serializer.data["parents_username"])>2)):
        return Response("invalid request",status=400)

    if len(serializer.data["parents_username"])==2:
        if parent2.gender==parent1.gender:
            return Response("invalid request",status=400)

    id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    fml = family(family_id=id, member_count= len(serializer.data["parents_username"])+len(serializer.data["childs_username"]))
    fml.save()

    for i in serializer.data["parents_username"]:
        usr = user.objects.get(username=i)
        usr.parent_of = fml
        usr.save()

    for i in serializer.data["childs_username"]:
        usr = user.objects.get(username=i)
        usr.child_of = fml
        usr.save()
    return Response("created", status=201)

    





chema = openapi.Schema(description="reeturns string which describes status", type=openapi.TYPE_STRING)
res400 = openapi.Response("invalid request", schema=chema)
res401 = openapi.Response("Unauthorized client", schema=chema)
res200 = openapi.Response("package selected or changed", schema=chema)
@swagger_auto_schema(methods=['post'], request_body=CreateFamilySerializer, responses={400: res400, 401: res401, 20: res200})
@api_view(('POST',))
def select_package(request):# selecting or changing package of a sonn
    serializer = PackageSelectionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response("invalid request", status=400)   
    
    usr = request.user
    child = user.objects.get(username=serializer.data["child_username"])
    if usr.parent_of != child.child_of:
        return Response("Unauthorized client", status=401)

    pg = package.objects.get(type=serializer.data["package_type"])
    child.pg = pg
    child.save()
    return Response("successful operation", status=200)
    



chema = openapi.Schema(description="reeturns string which describes status", type=openapi.TYPE_STRING)
res400 = openapi.Response("invalid request", schema=chema)
res401 = openapi.Response("Unauthorized client", schema=chema)
res200 = openapi.Response("package deleted", schema=chema)
@api_view(('POST',))
def delete_package(request):
    serializer = PackageDeletionSerializer(data=request.data)
    if not serializer.is_valid():
        return Response("invalid request", status=400)   
    
    usr = request.user
    child = user.objects.get(username=serializer.data["child_username"])
    if usr.parent_of != child.child_of:
        return Response("Unauthorized client", status=401)
        
    child.pg = None
    child.save()
    return Response("package deleted", status=200)

