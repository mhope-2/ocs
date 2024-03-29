from django.contrib import admin
from django.urls import path, include
from .views import InvoiceViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('invoices', InvoiceViewSet, basename='Invoices')


urlpatterns = [
    path('', include(router.urls)),

    # products
    path('invoices', InvoiceViewSet.as_view({
        'get': 'list',
    })),
    path('invoices/create', InvoiceViewSet.as_view({
        'post': 'create',
    })),
    path('invoices/<str:pk>/update', InvoiceViewSet.as_view({
        'put': 'update',
    })),
    path('invoices/<str:pk>', InvoiceViewSet.as_view({
        'get': 'retrieve',
    })),
    path('invoices/<str:pk>/delete', InvoiceViewSet.as_view({
        'delete': 'destroy'
    })),

    

]