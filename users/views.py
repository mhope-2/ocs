from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
import datetime
from rest_framework import generics, permissions
from rest_framework.decorators import action

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from rest_framework.authtoken.models import Token

from .models import User, Role
from .serializers import (
    RoleSerializer, UserSerializer, RequestPasswordResetEmailSerializer, 
    SetNewPasswordSerializer
)
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


import logging
from pathlib import Path
# Create your views here.

ROOT_DIR = Path('__file__').resolve().parent

logging.basicConfig(filename=str(ROOT_DIR)+'/logs/amata.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    level=logging.DEBUG)



class RoleViewSet(viewsets.ViewSet):
    def list(self, request): 
        roles = Role.objects.filter(deleted_at=None)
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ViewSet):

    # permission_classes = (permissions.IsAuthenticated,)

    def list(self, request): 
        users = User.objects.filter(deleted_at=None)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def create(self, request): 
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logging.debug(str(serializer))
            return Response({"response": "User registration successful"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"response": "Error Registering User"}, status=status.HTTP_400_BAD_REQUEST)
    
    @csrf_exempt
    def update(self, request, pk=None): 
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(instance=user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"response": "Error Updating User"}, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
            serializer = User(instance=user)
            request_instance = dict(serializer.data)
            request_instance['deleted_at'] = datetime.datetime.now()
            serializer = User(instance=user, data=request_instance)
            serializer.is_valid(raise_exception=True)
            serializer.deleted_at=datetime.datetime.now()
            serializer.save()
            return Response({"response":"User {} deleted successfully".format(user.username)}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_204_NO_CONTENT)


    @csrf_exempt
    @action(detail=False, methods=['post'])
    def fetch(self, request):
        try:
            user_id = Token.objects.get(key=request.data["auth_token"]).user_id
            user = User.objects.get(id=user_id,deleted_at=None)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"response": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer

    def post(self, request, *args, **kwargs):
        data = {'request':request, 'data': request.data}
        serializer = self.serializer_class(data=request.data)

        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request ).domain
            relative_link = reverse('password-reset-confirm', kwargs={'uidb64':uidb64,'token':token})
            absurl = 'http://'+str("https://amata.com")+str(relative_link)
            email_body = 'Hi \nUse the link below to reset your password.\n ' + str(absurl)
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset Password'}
            Util.send_email(data)
            # serializer.is_valid(raise_exception=True)
            # serializer.save()
            return Response({"response": "Password reset email sent"}, status=status.HTTP_200_OK)
        else:
            return Response({"response": "Email doesn't exist"})
        
 

class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"response": "Token is not valid. Please request a new one."}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({"response": "Password reset link is valid", "success":True, "uidb64":uidb64, "token": token }, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as e:
            return Response({"response": "Token is not valid. Please request a new one."}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"response": "Password Reset was Successful", "success": True}, status=status.HTTP_200_OK)
