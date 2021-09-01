from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
import datetime
# import pandas as pd

from rest_framework import generics, permissions
from .models import Receipt
from quotations.models import Quotation

from .serializers import ReceiptSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import random

from rest_framework.decorators import action
import logging
from pathlib import Path
# Create your views here.

ROOT_DIR = Path('__file__').resolve().parent

logging.basicConfig(filename=str(ROOT_DIR)+'/logs/amata.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    level=logging.DEBUG)


class ReceiptViewSet(viewsets.ViewSet):

    def list(self, request): 
        try:
            receipt = Receipt.objects.filter(deleted_at=None)
            serializer = ReceiptSerializer(receipt, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request): 
        try:
            receipt = request.data

            # receipt serializer
            random_pay_code = random.randint(10000,900000)
            receipt["receipt_no"] = "REC"+str(random_pay_code)

            if not Payment.objects.filter(payment_no=str(receipt['payment_no'])).exists():
                return Response({"response":"Invalid Payment Number"}, status=status.HTTP_400_BAD_REQUEST)
             
            receipt_serializer = ReceiptSerializer(data=receipt)
            receipt_serializer.is_valid(raise_exception=True)
            receipt_serializer.save()

            return Response({"receipt": receipt}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None): 
        try:
            receipt = Receipt.objects.get(id=pk, deleted_at=None)
            receipt_serializer = ReceiptSerializer(receipt)

            return Response(receipt_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None): 
        try:
            # receipt
            receipt = Receipt.objects.get(id=pk)

            receipt_serializer = ReceiptSerializer(instance=receipt, data=request.data)
            receipt_serializer.is_valid(raise_exception=True)
            receipt_serializer.save()

            return Response(request.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None):
        try:
            receipt = Receipt.objects.get(id=pk)
            serializer = InvoicesSerializer(instance=receipt)
            request_instance = dict(serializer.data)
            request_instance['deleted_at'] = datetime.datetime.now()
            receipt_serializer = ReceiptSerializer(instance=receipt, data=request_instance)
            receipt_serializer.is_valid(raise_exception=True)
            receipt_serializer.deleted_at=datetime.datetime.now()
            receipt_serializer.save()

            return Response({"response":"Invoice deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)


    # @csrf_exempt
    @action(detail=False, methods=['get'])
    def fetchByNo(self, request, pk=None):
        try:
            receipt = Receipt.objects.get(receipt_no=pk, deleted_at=None)
            serializer = ReceiptSerializer(receipt)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"response": str(e)}, status=status.HTTP_400_BAD_REQUEST)