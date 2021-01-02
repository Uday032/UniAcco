
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken
from django.contrib.auth.hashers import check_password
from django.contrib import auth
from django.conf import settings

# models
from django.contrib.auth.models import User

# self defined functions 
import jwt

@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    serializer = UserSerializer(request.username)
    return Response(serializer.data)


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
        print(request.data['username'])
        user = User.objects.filter(username=request.data['username'])
        serializer = UserSerializer(user, many=True)
        if(len(serializer.data)==0):
            return Response("Wrong UserName", status=status.HTTP_400_BAD_REQUEST)
        passcheck = check_password(request.data['password'], serializer.data[0]['password'])
        if(passcheck!=True):
            return Response("Wrong Password", status=status.HTTP_400_BAD_REQUEST)
        payload = {
            'user_id': serializer.data[0]['id'],
            'username': request.data['username'],
            'exp': 1609569034,
            'email': serializer.data[0]['email']
        }
        auth_token = jwt.encode(payload, settings.JWT_AUTH['JWT_SECRET_KEY'])
        data = {'user': serializer.data[0], 'token': auth_token}
        return Response(data, status=status.HTTP_200_OK)