"""ocs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from users.views import (
    RequestPasswordResetEmail, SetNewPasswordAPIView, PasswordTokenCheckAPI
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('rest_auth.urls')),
    path('rest-auth-reg/', include('rest_auth.registration.urls')),
    
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('clothes.urls')),
    path('api/v1/', include('customers.urls')),

    # path('api/v1/', include('djoser.urls')),

    path('api/v1/password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('api/v1/request-reset-email/', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('api/v1/password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
]

