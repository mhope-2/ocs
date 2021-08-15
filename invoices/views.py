from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
import datetime
# import pandas as pd

from rest_framework import generics, permissions
from .models import InvoiceItems, Invoices

from .serializers import InvoiceItemsSerializer, InvoiceSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import random


import logging
from pathlib import Path
# Create your views here.

ROOT_DIR = Path('__file__').resolve().parent

logging.basicConfig(filename=str(ROOT_DIR)+'/logs/amata.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    level=logging.DEBUG)


class InvoicesViewSet(viewsets.ViewSet):

    def list(self, request): 
        try:
            invoice = Invoices.objects.filter(deleted_at=None)
            serializer = InvoiceSerializer(invoice, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request): 
        try:
            invoice = request.data["invoice"]
            invoice_items = request.data["invoice_items"]

            # invoice serializer
            random_bk_code = random.randint(10000,900000)
            invoice["invoice_no"] = "INV"+str(random_bk_code)
            quotation_serializer = InvoiceSerializer(data=invoice)
            quotation_serializer.is_valid(raise_exception=True)
            quotation_serializer.save()
            
            # invoice items
            saved_quotation_booking_code = str(Invoices.objects.last())
            for item in invoice_items:
                item["invoice_no"] = saved_quotation_booking_code
                invoice_item_serializer = QuotationItemsSerializer(data=item)
                invoice_item_serializer.is_valid(raise_exception=True)
                invoice_item_serializer.save()
            # logging.debug(str(quotation_serializer))


            return Response({"invoice": invoice, "invoice_items": invoice_items}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None): 
        try:
            invoice = Invoices.objects.get(id=pk, deleted_at=None)
            quotation_serializer = InvoiceSerializer(invoice)

            # invoice items list
            invoice_items_list = []

            invoice_items = QuotationItems.objects.filter(invoice_no=invoice.invoice_no)
            for item in invoice_items:
                invoice_items_serializer = QuotationItemsSerializer(item)
                invoice_items_list.append(invoice_items_serializer.data)

            return Response({"invoice": quotation_serializer.data, "invoice_items": invoice_items_list}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None): 
        try:
            # invoice
            invoice = Invoices.objects.get(id=pk)
            invoice_items = QuotationItems.objects.filter(invoice_no=invoice.invoice_no)

            quotation_serializer = InvoiceSerializer(instance=invoice, data=request.data["invoice"])
            quotation_serializer.is_valid(raise_exception=True)
            quotation_serializer.save()

            # # invoice items
            for index,item in enumerate(invoice_items):
                invoice_item_serializer = QuotationItemsSerializer(instance = item, data=request.data["invoice_items"][index])
                invoice_item_serializer.is_valid(raise_exception=True)
                invoice_item_serializer.save()

            return Response(request.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None):
        try:
            invoice = Invoices.objects.get(id=pk)
            print(invoice.invoice_no)
            serializer = InvoicesSerializer(instance=invoice)
            request_instance = dict(serializer.data)
            request_instance['deleted_at'] = datetime.datetime.now()
            quotation_serializer = InvoiceSerializer(instance=invoice, data=request_instance)
            quotation_serializer.is_valid(raise_exception=True)
            quotation_serializer.deleted_at=datetime.datetime.now()
            quotation_serializer.save()

            # 
            invoice_items = QuotationItems.objects.get(invoice_no=invoice.invoice_no)
            for item in invoice_items:
                serializer = QuotationItemsSerializer(instance=item)
                request_instance = dict(serializer.data)
                request_instance['deleted_at'] = datetime.datetime.now()
                invoice_item_serializer = QuotationItemsSerializer(instance=item, data=request_instance)
                invoice_item_serializer.is_valid(raise_exception=True)
                invoice_item_serializer.deleted_at=datetime.datetime.now()
                invoice_item_serializer.save()

            return Response({"response":"Invoice deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)
