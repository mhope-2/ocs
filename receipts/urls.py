from django.contrib import admin
from django.urls import path, include
from .views import ReceiptViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('receipts', ReceiptViewSet, basename='Receipts')


urlpatterns = [
    path('', include(router.urls)),

    # receipts
    path('receipts', ReceiptViewSet.as_view({
        'get': 'list',
    })),
    path('receipts/create', ReceiptViewSet.as_view({
        'post': 'create',
    })),
    path('receipts/<str:pk>/update', ReceiptViewSet.as_view({
        'put': 'update',
    })),
    path('receipts/<str:pk>', ReceiptViewSet.as_view({
        'get': 'retrieve',
    })),
    path('receipts/<str:pk>/delete', ReceiptViewSet.as_view({
        'delete': 'destroy'
    })),

    path('receipt/by/number/<str:pk>', ReceiptViewSet.as_view({
        'get': 'fetchByNo'
    })),

    

    

]