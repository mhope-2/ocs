from django.contrib import admin
from django.urls import path, include
from .views import PaymentViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('payments', PaymentViewSet, basename='Payments')


urlpatterns = [
    path('', include(router.urls)),

    # payments
    path('payments', PaymentViewSet.as_view({
        'get': 'list',
    })),
    path('payments/create', PaymentViewSet.as_view({
        'post': 'create',
    })),
    path('payments/<str:pk>/update', PaymentViewSet.as_view({
        'put': 'update',
    })),
    path('payments/<str:pk>', PaymentViewSet.as_view({
        'get': 'retrieve',
    })),
    path('payments/<str:pk>/delete', PaymentViewSet.as_view({
        'delete': 'destroy'
    })),

    path('payment/by/number/<str:pk>', PaymentViewSet.as_view({
        'get': 'fetchByNo'
    })),

    

    

]