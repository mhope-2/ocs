from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
import datetime
# import pandas as pd

from rest_framework import generics, permissions
from .models import Category, Product

from .serializers import ProductSerializer, CategorySerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



import logging
from pathlib import Path
# Create your views here.

ROOT_DIR = Path('__file__').resolve().parent

logging.basicConfig(filename=str(ROOT_DIR)+'/logs/ocs.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    level=logging.DEBUG)


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class CategoryViewSet(viewsets.ViewSet):

    # permission_classes = (permissions.IsAuthenticated,)

    def list(self, request): 
        try:
            categories = Category.objects.filter(deleted_at=None)
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def create(self, request): 
        try:
            serializer = CategorySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logging.debug(str(serializer))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None): 
        try:
            category = ClotheCategories.objects.get(id=pk, deleted_at=None)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def update(self, request, pk=None): 
        try:
            category = Category.objects.get(id=pk)
            serializer = CategorySerializer(instance=category, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"response": "Category has been updated successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def destroy(self, request, pk=None):
        try:
            category = categories.objects.get(id=pk)
            serializer = CategorySerializer(instance=category)
            request_instance = dict(serializer.data)
            request_instance['deleted_at'] = datetime.datetime.now()
            serializer = CategorySerializer(instance=category, data=request_instance)
            serializer.is_valid(raise_exception=True)
            serializer.deleted_at=datetime.datetime.now()
            serializer.save()
            return Response({"response":"Clothe Category {} deleted successfully".format(category.name)}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)


# 
class ProductViewSet(viewsets.ViewSet):

    # permission_classes = (permissions.IsAuthenticated,)

    def list(self, request): 
        try:
            clothes = Clothes.objects.filter(deleted_at=None)
            serializer = ProductSerializer(clothes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request): 
        try:
            serializer = ProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            logging.debug(str(serializer))
            return Response({"response": "Clothe created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None): 
        try:
            clothe = Clothes.objects.get(id=pk, deleted_at=None)
            serializer = ProductSerializer(Clothe)
            return Response(serializer.data)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None): 
        try:
            clothe = Clothes.objects.get(id=pk)
            serializer = ProductSerializer(instance=Clothe, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"response": "Clothe updated successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
    def destroy(self, request, pk=None):
        try:
            clothe = Clothes.objects.get(id=pk)
            serializer = ProductSerializer(instance=Clothe)
            request_instance = dict(serializer.data)
            request_instance['deleted_at'] = datetime.datetime.now()
            serializer = ProductSerializer(instance=Clothe, data=request_instance)
            serializer.is_valid(raise_exception=True)
            serializer.deleted_at=datetime.datetime.now()
            serializer.save()
            return Response({"response":"Clothe deleted successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(str(e))
            return Response({"response":str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
import pandas as pd
import numpy as np

class FileUploadView(APIView):

    parser_classes = (MultiPartParser,)

    def post(self, request, format=None):
        try:
            file_obj = pd.read_excel(request.data['clothes'])
            df = pd.DataFrame(file_obj)
            df = df.replace(np.nan, '', regex=True)
            data = df.to_dict(orient='records')

            for item in data:
                if not ClotheCategories.objects.filter(name=item['category']).exists():
                    return Response({"response": "Bulk Upload Sheet Contains an Invalid Category {}. Kindly Add the Category(ies).".format(item['category'])}, status=status.HTTP_400_BAD_REQUEST)
                
            # check for category to int
            for item in data:
                category_id = ClotheCategories.objects.get(name=item['category']).id
                item['category'] = int(category_id)

                # check for created by

                serializer = ProductSerializer(data=item)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            return Response({"response": "Successfully Uploaded Clothes"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"response": str(e)}, status=status.HTTP_204_NO_CONTENT)
