from django.contrib import admin
from django.urls import path, include
from .views import (
                    CategoriesViewSet, ProductsViewSet,
                    FileUploadView
                    )
from rest_framework import routers


router = routers.DefaultRouter()
router.register('products/categories', CategoriesViewSet, basename='Categories')
router.register('products', ProductsViewSet, basename='products')


urlpatterns = [
    path('', include(router.urls)),

    # product categories 
    path('products/categories', CategoriesViewSet.as_view({
        'get': 'list',
    })),
    path('products/categories/create', CategoriesViewSet.as_view({
        'post': 'create',
    })),
    path('product/categories/<str:pk>', CategoriesViewSet.as_view({
        'get': 'retrieve',
        'patch': 'update',
    })),
     path('product/categories/destroy/<str:pk>', CategoriesViewSet.as_view({
        'delete': 'destroy'
    })),



    # products
    path('products', ProductsViewSet.as_view({
        'get': 'list',
    })),
    path('products/create', ProductsViewSet.as_view({
        'post': 'create',
    })),
    path('products/<str:pk>/update', ProductsViewSet.as_view({
        'put': 'update',
    })),
    path('products/<str:pk>', ProductsViewSet.as_view({
        'get': 'retrieve',
    })),
    path('products/<str:pk>/delete', ProductsViewSet.as_view({
        'delete': 'destroy'
    })),


    # Bulk
    # path('products/bulk/upload', productsViewSet.as_view({
        # 'post': 'bulk_upload',
    # })),


    path('products/bulk/upload', FileUploadView.as_view(), name='products_bulk_upload'),
    

]