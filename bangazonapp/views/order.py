import json
from django.http import HttpResponse
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from bangazonapp.models import Customer
from bangazonapp.models import Order, PaymentType
from .payment_type import PaymentTypeSerializer


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    # payment_type = PaymentTypeSerializer()

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'created_at', 'customer', 'payment_type')
        depth = 1

class Orders(ViewSet):

    def create(self, request):
        """Handle POST operations"""

        order = Order.objects.create(
            customer = Customer.objects.get(pk = request.data["customer_id"]),
            payment_type = PaymentType.objects.get(pk = request.data["payment_type_id"])
        )

        serializer = OrderSerializer(order, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        order = Order.objects.get(pk=pk)
        payment_type = PaymentType.objects.get(pk=request.data["payment_type_id"])
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
            order.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        orders = Order.objects.all()  # This is my query to the database
        serializer = OrderSerializer(
            orders, many=True, context={'request': request})
        return Response(serializer.data)
