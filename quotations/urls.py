from django.contrib import admin
from django.urls import path, include
from .views import QuotationViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register('quotations', QuotationViewSet, basename='Quotations')


urlpatterns = [
    path('', include(router.urls)),

    # products
    path('quotations', QuotationViewSet.as_view({
        'get': 'list',
    })),
    path('quotations/create', QuotationViewSet.as_view({
        'post': 'create',
    })),
    path('quotations/<str:pk>/update', QuotationViewSet.as_view({
        'put': 'update',
    })),
    path('quotations/<str:pk>', QuotationViewSet.as_view({
        'get': 'retrieve',
    })),
    path('quotations/<str:pk>/delete', QuotationViewSet.as_view({
        'delete': 'destroy'
    })),

    

]