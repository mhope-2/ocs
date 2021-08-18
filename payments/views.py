from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
import datetime
# import pandas as pd

from rest_framework import generics, permissions
from .models import Invoice, Payment
from quotations.models import Quotation

from .serializers import PaymentSerializer
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


class PaymentsViewSet(viewsets.ViewSet):

    def list(self, request): 
        try:
            payment = Payment.objects.filter(deleted_at=None)
            serializer = PaymentSerializer(payment, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request): 
        try:
            payment = request.data

            # payment serializer
            random_pay_code = random.randint(10000,900000)
            payment["payment_no"] = "PAY"+str(random_pay_code)

            if not Invoice.objects.filter(invoice_no=str(payment['invoice_no'])).exists():
                return Response({"response":"Invalid Invoice Number"}, status=status.HTTP_400_BAD_REQUEST)
             
            payment_serializer = PaymentSerializer(data=payment)
            payment_serializer.is_valid(raise_exception=True)
            payment_serializer.save()

            Invoice.objects.filter(invoice_no=str(payment['invoice_no'])).update(status='paid', date_paid=datetime.datetime.now())

            return Response({"payment": payment}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None): 
        try:
            payment = Payment.objects.get(id=pk, deleted_at=None)
            payment_serializer = PaymentSerializer(payment)

            return Response(payment_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None): 
        try:
            # payment
            payment = Payment.objects.get(id=pk)

            payment_serializer = PaymentSerializer(instance=payment, data=request.data)
            payment_serializer.is_valid(raise_exception=True)
            payment_serializer.save()

            return Response(request.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None):
        try:
            payment = Payment.objects.get(id=pk)
            serializer = InvoicesSerializer(instance=payment)
            request_instance = dict(serializer.data)
            request_instance['deleted_at'] = datetime.datetime.now()
            payment_serializer = PaymentSerializer(instance=payment, data=request_instance)
            payment_serializer.is_valid(raise_exception=True)
            payment_serializer.deleted_at=datetime.datetime.now()
            payment_serializer.save()

            return Response({"response":"Invoice deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)


    # @csrf_exempt
    @action(detail=False, methods=['get'])
    def fetchByNo(self, request, pk=None):
        try:
            payment = Payment.objects.get(payment_no=pk, deleted_at=None)
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"response": str(e)}, status=status.HTTP_400_BAD_REQUEST)