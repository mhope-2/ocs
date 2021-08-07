from django.contrib import admin
from django.urls import path, include
from .views import (
                    CustomerViewSet
                    )

from rest_framework import routers


router = routers.DefaultRouter()
router.register('customers', CustomerViewSet, basename='Customer')


urlpatterns = [
    path('', include(router.urls)),
    path('customers', CustomerViewSet.as_view({
        'get': 'list',
    })),
    path('customers/create', CustomerViewSet.as_view({
        'post': 'create',
    })),
    path('customers/<str:pk>', CustomerViewSet.as_view({
        'get': 'retrieve',
        'patch': 'update',
        'delete': 'destroy',
    })),
    
    # path('users/get', UserViewSet.as_view({
    #     'get': 'fetchUserData'
    #     })),
]
