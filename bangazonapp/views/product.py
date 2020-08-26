from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapp.models import Product, Customer, ProductType


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
    # customer_url = serializers.HyperlinkedIdentityField(
    #     view_name="customer",
    #     many=False,
    #     required=True,
    #     lookup_field="pk"
    # )

    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
<<<<<<< HEAD
        fields = ("id", "url", "title", "price", "description",
                  "quantity", "location", "image_path", "customer")
=======
        fields = ("id", "url", "title", "price", "description", "quantity", "location", "image_path", "customer", "product_type")
>>>>>>> master
        depth = 2


class Products(ViewSet):
    # """""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Product instance
        """
        customer = Customer.objects.get(user_id=request.user.id)
        product_type = ProductType.objects.get(
            pk=request.data['product_type_id'])

        product = Product.objects.create(
            title=request.data["title"],
            price=request.data["price"],
            description=request.data["description"],
            quantity=request.data["quantity"],
            location=request.data["location"],
            image_path=request.data["image_path"],
            product_type=product_type,
            customer=customer
        )
        serializer = ProductSerializer(product, context={'request': request})

        return Response(serializer.data, content_type='application/json')

    def retrieve(self, request, pk=None):
        """Handle GET operation

        Returns:
            Response -- JSON serialized product instance
        """
        try:
            # user = User.objects.get(pk=pk)
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(
                product, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for products

        Returns:
            Response -- Empty body with 204 status code
        """

        product = Product.objects.get(pk=pk)
        product.title = request.data["title"],
        product.price = request.data["price"],
        product.description = request.data["description"],
        product.quantity = request.data["quantity"],
        product.location = request.data["location"],
        product.image_path = request.data["image_path"],
        product.product_type = request.data["product_type"]
        product.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a product

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            product = Product.objects.get(pk=pk)
            product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Product.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        # except Exception as ex:
        #     return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to product resource

        Returns:
            Response -- JSON serialized list of products
        """
        products = Product.objects.all()
        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)
