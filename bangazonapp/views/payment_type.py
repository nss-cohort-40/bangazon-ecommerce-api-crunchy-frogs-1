from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapp.models import PaymentType, Customer
from django.contrib.auth.models import User

class PaymentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='paymenttype',
            lookup_field='id'
        )
        fields = ('id', 'merchant_name', 'account_number',
                  'expiration_date', 'customer')
        depth = 1

def getUser(request):
    user = User.objects.get(pk=request.user.id)
    customer = Customer.objects.get(pk=user.customer.id)
    return customer

class PaymentTypes(ViewSet):

    def create(self, request):
        """ POST a PaymentType """

        customer = Customer.objects.get(user=request.auth.user.id)
        payment_type = PaymentType.objects.create(
            merchant_name=request.data['merchant_name'],
            account_number=request.data['account_number'],
            expiration_date=request.data['expiration_date'],
            customer=customer,
        )

        serializer = PaymentTypeSerializer(
            payment_type, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """ GET a PaymentType """

        try:
            payment_type = PaymentType.objects.get(pk=pk)
            serializer = PaymentTypeSerializer(
                payment_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """ PUT a PaymentType """

        payment_type = PaymentType.objects.get(pk=pk)
        payment_type.merchant_name = request.data["merchant_name"]
        payment_type.account_number = request.data["account_number"]
        payment_type.expiration_date = request.data["expiration_date"]
        payment_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """ DELETE a PaymentType """

        try:
            payment_type = PaymentType.objects.get(pk=pk)
            payment_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except PaymentType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """ GET all PaymentTypes """

        payment_types = PaymentType.objects.all()

        # Support filtering attractions by area id
        customer = getUser(request)
        if customer is not None:
            payment_types = payment_types.filter(customer__id=customer.id)

        serializer = PaymentTypeSerializer(
            payment_types, many=True, context={'request': request})
        return Response(serializer.data)
