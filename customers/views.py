from django.shortcuts import render
from .models import Customer
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import CustomerSerializer
from django.views.decorators.csrf import csrf_exempt

import datetime

import logging
from pathlib import Path
# Create your views here.

ROOT_DIR = Path('__file__').resolve().parent

logging.basicConfig(filename=str(ROOT_DIR)+'/logs/ocs.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    level=logging.DEBUG)
# Create your views here.


class CustomerViewSet(viewsets.ViewSet):

    # permission_classes = (permissions.IsAuthenticated,)

    def list(self, request): 
        users = Customer.objects.filter(deleted_at=None)
        serializer = CustomerSerializer(users, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def create(self, request): 
        try:
            serializer = CustomerSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logging.debug(str(serializer))
            return Response({"response": "Customer registration successful"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"response": "Error Registering Customer"}, status=status.HTTP_400_BAD_REQUEST)
    

    def retrieve(self, request, pk=None): 
        try:
            customer = Customer.objects.get(id=pk, deleted_at=None)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def update(self, request, pk=None): 
        try:
            user = Customer.objects.get(id=pk)
            serializer = CustomerSerializer(instance=user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"response":"Customer updated successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"response": "Error Updating Customer"}, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def destroy(self, request, pk=None):
        try:
            customer = Customer.objects.get(id=pk)
            serializer = CustomerSerializer(instance=customer)
            request_instance = dict(serializer.data)
            request_instance['deleted_at'] = datetime.datetime.now()
            serializer = CustomerSerializer(instance=customer, data=request_instance)
            serializer.is_valid(raise_exception=True)
            serializer.deleted_at=datetime.datetime.now()
            serializer.save()
            return Response({"response":"Customer with name {} {} {} deleted successfully".format(
                customer.first_name, customer.middle_name, customer.last_name)}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_204_NO_CONTENT)


    # @csrf_exempt
    # @action(detail=False, methods=['post'])
    # def fetch(self, request):
    #     try:
    #         user_id = Token.objects.get(key=request.data["auth_token"]).user_id
    #         user = Customer.objects.get(id=user_id,deleted_at=None)
    #         serializer = CustomerSerializer(user)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({"response": str(e)}, status=status.HTTP_400_BAD_REQUEST)