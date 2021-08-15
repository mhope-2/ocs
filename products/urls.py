from django.contrib import admin
from django.urls import path, include
from .views import (
                    CategoryViewSet, ProductViewSet,
                    FileUploadView
                    )
from rest_framework import routers


router = routers.DefaultRouter()
router.register('products/categories', CategoryViewSet, basename='Categories')
router.register('products', ProductViewSet, basename='products')


urlpatterns = [
    path('', include(router.urls)),

    # product categories 
    path('products/categories', CategoryViewSet.as_view({
        'get': 'list',
    })),
    path('products/categories/create', CategoryViewSet.as_view({
        'post': 'create',
    })),
    path('product/categories/<str:pk>', CategoryViewSet.as_view({
        'get': 'retrieve',
        'patch': 'update',
    })),
     path('product/categories/destroy/<str:pk>', CategoryViewSet.as_view({
        'delete': 'destroy'
    })),



    # products
    path('products', ProductViewSet.as_view({
        'get': 'list',
    })),
    path('products/create', ProductViewSet.as_view({
        'post': 'create',
    })),
    path('products/<str:pk>/update', ProductViewSet.as_view({
        'put': 'update',
    })),
    path('products/<str:pk>', ProductViewSet.as_view({
        'get': 'retrieve',
    })),
    path('products/<str:pk>/delete', ProductViewSet.as_view({
        'delete': 'destroy'
    })),


    # Bulk
    # path('products/bulk/upload', productsViewSet.as_view({
        # 'post': 'bulk_upload',
    # })),


    path('products/bulk/upload', FileUploadView.as_view(), name='products_bulk_upload'),
    

]