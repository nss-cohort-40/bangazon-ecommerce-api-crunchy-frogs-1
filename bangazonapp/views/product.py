from django.http import HttpResponseServerError
from django.http import HttpResponse
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
        fields = ('id', 'title', 'price', 'description', "quantity", "location", "image_path", "product_type")
        depth = 2

class Products(ViewSet):
    # """""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized User instance
        """

        product = Product.objects.create(
            title = request.data["title"],
            last_name = request.data["price"],
            description = request.data["description"],
            quantity = request.data["quantity"],
            location = request.data["location"],
            image_path = request.data["image_path"],
            product_type_id = request.data["product_type_id"],
        )

        return HttpResponse(data, content_type='application/json')

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            # user = User.objects.get(pk=pk)
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(customer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area

        Returns:
            Response -- Empty body with 204 status code
        """

        customer = Customer.objects.get(pk=pk)
        customer.address = request.data["address"]
        customer.phone_number = request.data["phone_number"]
        customer.save()

        user = User.objects.get(pk=customer.user.id)
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.username = request.data["username"]
        user.password = make_password(request.data["password"])
        user.email = request.data["email"]
        user.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            user = User.objects.get(pk=pk)
            user.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Customer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park areas resource

        Returns:
            Response -- JSON serialized list of park areas
        """
        customers = Customer.objects.all()  # This is my query to the database
        serializer = CustomerSerializer(
            customers, many=True, context={'request': request})
        return Response(serializer.data)
