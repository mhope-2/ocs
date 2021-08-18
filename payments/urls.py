from django.contrib import admin
from django.urls import path, include
from .views import PaymentsViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('payments', PaymentsViewSet, basename='Payments')


urlpatterns = [
    path('', include(router.urls)),

    # payments
    path('payments', PaymentsViewSet.as_view({
        'get': 'list',
    })),
    path('payments/create', PaymentsViewSet.as_view({
        'post': 'create',
    })),
    path('payments/<str:pk>/update', PaymentsViewSet.as_view({
        'put': 'update',
    })),
    path('payments/<str:pk>', PaymentsViewSet.as_view({
        'get': 'retrieve',
    })),
    path('payments/<str:pk>/delete', PaymentsViewSet.as_view({
        'delete': 'destroy'
    })),

    path('payment/by/number/<str:pk>', PaymentsViewSet.as_view({
        'get': 'fetchByNo'
    })),

    

    

]