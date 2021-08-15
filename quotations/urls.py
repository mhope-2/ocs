from django.contrib import admin
from django.urls import path, include
from .views import QuotationsViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('quotations', QuotationsViewSet, basename='Quotations')


urlpatterns = [
    path('', include(router.urls)),

    # products
    path('quotations', QuotationsViewSet.as_view({
        'get': 'list',
    })),
    path('quotations/create', QuotationsViewSet.as_view({
        'post': 'create',
    })),
    path('quotations/<str:pk>/update', QuotationsViewSet.as_view({
        'put': 'update',
    })),
    path('quotations/<str:pk>', QuotationsViewSet.as_view({
        'get': 'retrieve',
    })),
    path('quotations/<str:pk>/delete', QuotationsViewSet.as_view({
        'delete': 'destroy'
    })),

    

]