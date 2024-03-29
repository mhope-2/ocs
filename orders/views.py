from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
import datetime
# import pandas as pd

from rest_framework import generics, permissions
from .models import OrderItems, Order

from rest_framework.decorators import action


from .serializers import OrderItemsSerializer, OrderSerializer
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


class OrderViewSet(viewsets.ViewSet):

    def list(self, request): 
        try:
            order = Orders.objects.filter(deleted_at=None)
            serializer = OrderSerializer(order, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request): 
        try:
            order = request.data["order"]
            order_items = request.data["order_items"]

            # order serializer
            random_bk_code = random.randint(10000,900000)
            order["order_no"] = "ORD"+str(random_bk_code)
            order_serializer = OrderSerializer(data=order)
            order_serializer.is_valid(raise_exception=True)
            order_serializer.save()
            
            # order items
            saved_order_booking_code = str(Orders.objects.last())
            for item in order_items:
                item["order_no"] = saved_order_booking_code
                order_item_serializer = OrderItemsSerializer(data=item)
                order_item_serializer.is_valid(raise_exception=True)
                order_item_serializer.save()
            # logging.debug(str(order_serializer))


            return Response({"order": order, "order_items": order_items}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None): 
        try:
            order = Orders.objects.get(id=pk, deleted_at=None)
            order_serializer = OrderSerializer(order)

            # order items list
            order_items_list = []

            order_items = OrderItems.objects.filter(quotation_no=order.quotation_no)
            for item in order_items:
                order_items_serializer = OrderItemsSerializer(item)
                order_items_list.append(order_items_serializer.data)

            return Response({"order": order_serializer.data, "order_items": order_items_list}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, pk=None): 
        try:
            # order
            order = Orders.objects.get(id=pk)
            order_items = OrderItems.objects.filter(quotation_no=order.quotation_no)

            order_serializer = OrderSerializer(instance=order, data=request.data["order"])
            order_serializer.is_valid(raise_exception=True)
            order_serializer.save()

            # # order items
            for index,item in enumerate(order_items):
                order_item_serializer = OrderItemsSerializer(instance = item, data=request.data["order_items"][index])
                order_item_serializer.is_valid(raise_exception=True)
                order_item_serializer.save()

            return Response(request.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None):
        try:
            order = Orders.objects.get(id=pk)
            serializer = OrderSerializer(instance=order)
            request_instance = dict(serializer.data)
            request_instance['deleted_at'] = datetime.datetime.now()
            order_serializer = OrderSerializer(instance=order, data=request_instance)
            order_serializer.is_valid(raise_exception=True)
            order_serializer.deleted_at=datetime.datetime.now()
            order_serializer.save()

            # 
            order_items = OrderItems.objects.filter(quotation_no=order.quotation_no)
            for item in order_items:
                serializer = OrderItemsSerializer(instance=item)
                request_instance = dict(serializer.data)
                request_instance['deleted_at'] = datetime.datetime.now()
                order_item_serializer = OrderItemsSerializer(instance=item, data=request_instance)
                order_item_serializer.is_valid(raise_exception=True)
                order_item_serializer.deleted_at=datetime.datetime.now()
                order_item_serializer.save()

            return Response({"response":"Order deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)


        # @csrf_exempt
    @action(detail=False, methods=['get'])
    def fetchByNo(self, request, pk=None):
        try:
            order = Order.objects.get(order_no=pk, deleted_at=None)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"response": str(e)}, status=status.HTTP_400_BAD_REQUEST)
