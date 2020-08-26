"""bangazonllc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from bangazonapp.models import Product, Order, ProductOrder
from bangazonapp.views import Customers, UserViewSet, PaymentTypes, ProductTypes, Products, ProductOrders, login_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'customer', Customers, 'customer')
router.register(r'users', UserViewSet, 'user')
router.register(r'product', Products, 'product')
router.register(r'payment_type', PaymentTypes, 'payment_type')
router.register(r'producttypes', ProductTypes, 'producttype')
router.register(r'productorders', ProductOrders, 'productorder')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', login_user),
]
