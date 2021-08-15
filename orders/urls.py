from django.contrib import admin
from django.urls import path, include
from .views import OrderViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('orders', OrderViewSet, basename='Quotations')


urlpatterns = [
    path('', include(router.urls)),

    # products
    path('orders', OrderViewSet.as_view({
        'get': 'list',
    })),
    path('orders/create', OrderViewSet.as_view({
        'post': 'create',
    })),
    path('orders/<str:pk>/update', OrderViewSet.as_view({
        'put': 'update',
    })),
    path('orders/<str:pk>', OrderViewSet.as_view({
        'get': 'retrieve',
    })),
    path('orders/<str:pk>/delete', OrderViewSet.as_view({
        'delete': 'destroy'
    })),

    

]