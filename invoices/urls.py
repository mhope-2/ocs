from django.contrib import admin
from django.urls import path, include
from .views import InvoicesViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('invoices', InvoicesViewSet, basename='Invoices')


urlpatterns = [
    path('', include(router.urls)),

    # products
    path('invoices', InvoicesViewSet.as_view({
        'get': 'list',
    })),
    path('invoices/create', InvoicesViewSet.as_view({
        'post': 'create',
    })),
    path('invoices/<str:pk>/update', InvoicesViewSet.as_view({
        'put': 'update',
    })),
    path('invoices/<str:pk>', InvoicesViewSet.as_view({
        'get': 'retrieve',
    })),
    path('invoices/<str:pk>/delete', InvoicesViewSet.as_view({
        'delete': 'destroy'
    })),

    

]