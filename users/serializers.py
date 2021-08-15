from rest_framework import serializers
from .models import User,Role
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .utils import Util 

import logging
from pathlib import Path
# Create your views here.

ROOT_DIR = Path('__file__').resolve().parent

logging.basicConfig(filename=str(ROOT_DIR)+'/logs/ocs.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    level=logging.DEBUG) 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = User.objects.make_random_password()
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        data = {
            'email_subject': "INT Clothing Store User Password",
            'email_body': str(password),
            'to_email': validated_data.pop('email')
        }
        try:
            Util.send_email(data)
            log("{}'s password sent successfully".format(user.username))
        except Exception as e:
            logging.error("Sending User Password Failed")

        return user


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=5)

    class Meta:
        fields = ['email',]


class SetNewPasswordSerializer(serializers.Serializer):    
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password','token','uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                AuthenticationFailed('The Password Reset Link is Invalid', 401)

            user.set_password(password)
            user.save()
        except Exception as e:
            AuthenticationFailed('The Password Reset Link is Invalid', 401)
        return super().validate(attrs)

