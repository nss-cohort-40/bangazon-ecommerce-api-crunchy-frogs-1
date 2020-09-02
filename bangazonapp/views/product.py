from django.http import HttpResponseServerError
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapp.models import Product, Customer, ProductType

class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ("id", "url", "title", "price", "description", "quantity",
                  "location", "image_path", "customer", "product_type")
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

        If no query parameters on request return all products without distinctions, otherwise
        return the all products with the kewword provided in the title

        Returns:
            Response -- JSON serialized list of products

        """
        products = Product.objects.all()
        search = self.request.query_params.get('search', None)
        display_amount = self.request.query_params.get('limit', None)
        sort = self.request.query_params.get('sort', None)
        product_type = self.request.query_params.get('product_type', None)

        if sort is not None:
            products = products.order_by(sort)
        if display_amount is not None:
            products = products[:int(display_amount)]
        if product_type is not None:
            products = products.filter(product_type__id=product_type)
        if search is not None:
            products = products.filter(title__contains=search)

        serializer = ProductSerializer(products, many=True, context={'request': request})

        return Response(serializer.data)
