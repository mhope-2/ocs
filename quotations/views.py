from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
import datetime
# import pandas as pd

from rest_framework import generics, permissions
from .models import QuotationItems, Quotations

from .serializers import QuotationItemsSerializer, QuotationSerializer
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


class QuotationViewSet(viewsets.ViewSet):

    def list(self, request): 
        try:
            quotation = Quotations.objects.filter(deleted_at=None)
            serializer = QuotationSerializer(quotation, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request): 
        try:
            quotation = request.data["quotation"]
            quotation_items = request.data["quotation_items"]

            # quotation serializer
            random_bk_code = random.randint(10000,900000)
            quotation["quotation_no"] = "QUOT"+str(random_bk_code)
            quotation_serializer = QuotationSerializer(data=quotation)
            quotation_serializer.is_valid(raise_exception=True)
            quotation_serializer.save()
            
            # quotation items
            saved_quotation_booking_code = str(Quotations.objects.last())
            for item in quotation_items:
                item["quotation_no"] = saved_quotation_booking_code
                quotation_item_serializer = QuotationItemsSerializer(data=item)
                quotation_item_serializer.is_valid(raise_exception=True)
                quotation_item_serializer.save()
            # logging.debug(str(quotation_serializer))


            return Response({"quotation": quotation, "quotation_items": quotation_items}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None): 
        try:
            quotation = Quotations.objects.get(id=pk, deleted_at=None)
            quotation_serializer = QuotationSerializer(quotation)

            # quotation items list
            quotation_items_list = []

            quotation_items = QuotationItems.objects.filter(quotation_no=quotation.quotation_no)
            for item in quotation_items:
                quotation_items_serializer = QuotationItemsSerializer(item)
                quotation_items_list.append(quotation_items_serializer.data)

            return Response({"quotation": quotation_serializer.data, "quotation_items": quotation_items_list}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None): 
        try:
            # quotation
            quotation = Quotations.objects.get(id=pk)
            quotation_items = QuotationItems.objects.filter(quotation_no=quotation.quotation_no)

            quotation_serializer = QuotationSerializer(instance=quotation, data=request.data["quotation"])
            quotation_serializer.is_valid(raise_exception=True)
            quotation_serializer.save()

            # # quotation items
            for index,item in enumerate(quotation_items):
                quotation_item_serializer = QuotationItemsSerializer(instance = item, data=request.data["quotation_items"][index])
                quotation_item_serializer.is_valid(raise_exception=True)
                quotation_item_serializer.save()

            return Response(request.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None):
        try:
            quotation = Quotations.objects.get(id=pk)
            serializer = QuotationSerializer(instance=quotation)
            request_instance = dict(serializer.data)
            request_instance['deleted_at'] = datetime.datetime.now()
            quotation_serializer = QuotationSerializer(instance=quotation, data=request_instance)
            quotation_serializer.is_valid(raise_exception=True)
            quotation_serializer.deleted_at=datetime.datetime.now()
            quotation_serializer.save()

            # 
            quotation_items = QuotationItems.objects.filter(quotation_no=quotation.quotation_no)
            for item in quotation_items:
                serializer = QuotationItemsSerializer(instance=item)
                request_instance = dict(serializer.data)
                request_instance['deleted_at'] = datetime.datetime.now()
                quotation_item_serializer = QuotationItemsSerializer(instance=item, data=request_instance)
                quotation_item_serializer.is_valid(raise_exception=True)
                quotation_item_serializer.deleted_at=datetime.datetime.now()
                quotation_item_serializer.save()

            return Response({"response":"Quotation deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)
