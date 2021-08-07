from django.contrib import admin
from django.urls import path, include
from .views import (
                    UserViewSet, RoleViewSet
                    )
from .views import RequestPasswordResetEmail 

from rest_framework import routers


router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='User')
router.register('roles', RoleViewSet, basename='Role')


urlpatterns = [
    path('', include(router.urls)),
    path('users', UserViewSet.as_view({
        'get': 'list',
    })),
    path('users/create', UserViewSet.as_view({
        'post': 'create',
    })),
    path('users/<str:pk>', UserViewSet.as_view({
        'patch': 'update',
        'delete': 'destroy',
    })),
    path('user/fetch', UserViewSet.as_view({
        'post': 'fetch',
    })),
    # path('users/get', UserViewSet.as_view({
    #     'get': 'fetchUserData'
    #     })),


    # roles
    path('roles', RoleViewSet.as_view({
        'get': 'list',
    })),

]