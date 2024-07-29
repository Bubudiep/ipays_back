from rest_framework import generics
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .serializers import *
from django.db import IntegrityError, transaction
from oauth2_provider.models import AccessToken
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
import numpy as np
import logging
logger = logging.getLogger(__name__)

def generate_response_json(result:str, message:str, data:dict={}):
    return {"result": result, "message": message, "data": data}

def to_json(result:str, message:str, data:dict={}):
    return {"result": result, "message": message, "data": data}

def unique(list1):
    x = np.array(list1)
    return np.unique(x)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
 
class StandardPagesPagination(PageNumberPagination):  
    page_size = 500
   
class AuthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)
     
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(to_json('success','User created successfully',serializer.data), status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(to_json('fail',str(e)), status=status.HTTP_400_BAD_REQUEST)
        return Response(to_json('fail',"Dữ liệu truyền vào không đúng định dạng",serializer.errors.items()), status=status.HTTP_400_BAD_REQUEST)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardPagesPagination
    authentication_classes = [OAuth2Authentication, SessionAuthentication, BasicAuthentication]
    @action(methods=['post'], detail=True, url_path='set-password', url_name='set-password')
    # detail=True: have pk parameter
    def set_password(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({"message": "Authentication credentials were not provided."}, status=401)
        user = self.get_object()
        if user.username!=request.user.username:
            return Response({"message": "Authentication credentials were not provided."}, status=401)
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            if serializer.validated_data['logout']==True:
                # delete token here
                AccessToken.objects.filter(user=user).delete()
            return Response(generate_response_json("OK",'Your password has been changed!',UserSerializer(user,many=False).data),status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def list(self, request):
        if not request.user.is_authenticated:
            return Response({"message": "Authentication credentials were not provided."}, status=401)
        queryset = self.get_queryset()
        queryset = queryset.get(username=request.user.username)
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data)
    