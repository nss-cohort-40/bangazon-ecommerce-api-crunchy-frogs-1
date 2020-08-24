from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from bangazonapp.models import Product


# Table Product {
#   Id int PK
#   Title varchar(50)
#   CustomerId int
#   Price decimal
#   Description varchar(255)
#   Quantity int
#   Location varchar(75)
#   ImagePath varchar(255)
#   CreatedAt datetime
#   ProductTypeId int
# }

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        fields = ('id', 'title', 'price', 'description', "quantity", "location", "image_path", "product_type_id")
        depth = 2
