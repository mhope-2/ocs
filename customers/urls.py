from django.contrib import admin
from django.urls import path, include
from .views import (
                    CustomerViewSet
                    )

from rest_framework import routers


router = routers.DefaultRouter()
router.register('customers', CustomerViewSet, basename='customers')


urlpatterns = [
    path('', include(router.urls)),
    path('customers', CustomerViewSet.as_view({
        'get': 'list',
    }), name='list'),

    path('customers/create', CustomerViewSet.as_view({
        'post': 'create',
    }), name='create'),

    path('customers/<str:pk>', CustomerViewSet.as_view({
        'get': 'retrieve',
    })),
    path('customers/<str:pk>', CustomerViewSet.as_view({
        'put': 'update',
    })),
    path('customers/<str:pk>', CustomerViewSet.as_view({
        'delete': 'destroy',
    })),
    
    # path('users/get', UserViewSet.as_view({
    #     'get': 'fetchUserData'
    #     })),
]
