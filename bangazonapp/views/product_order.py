from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapp.models import ProductOrder, Product, Order


class ProductOrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductOrder
        url = serializers.HyperlinkedIdentityField(
            view_name='productorder',
            lookup_field='id'
        )
        fields = ('id', 'url', 'product', 'order')
        depth = 1


class ProductOrders(ViewSet):

    def create(self, request):
        new_product_order = ProductOrder()

        product = Product.objects.get(pk=request.data['product_id'])
        new_product_order.product = product

        order = Order.objects.get(pk=request.data['order_id'])
        new_product_order.order = order
        new_product_order.save()

        serializer = ProductOrderSerializer(
            new_product_order, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            product_order = ProductOrder.objects.get(pk=pk)
            serializer = ProductOrderSerializer(
                product_order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def destroy(self, request, pk=None):

        try:
            product_order = ProductOrder.objects.get(pk=pk)
            product_order.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Itinerary.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):

        product_orders = ProductOrder.objects.all()
        
        product = self.request.query_params.get('product', None)
        if product is not None:
            product_orders = product_orders.filter(product__id=product)
        order = self.request.query_params.get('order', None)
        if order is not None:
            product_orders = product_orders.filter(order__id=order)
            
        serializer = ProductOrderSerializer(
            product_orders, many=True, context={'request': request})
        return Response(serializer.data)
