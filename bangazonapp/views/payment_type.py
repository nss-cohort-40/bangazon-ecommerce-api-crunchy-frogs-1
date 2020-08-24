from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapp.models import PaymentType, Customer




class PaymentTypeSerializer(serializers.HyperlinkedModelSerializer):


    class Meta:
        model = PaymentType
        url = serializers.HyperlinkedIdentityField(
            view_name='payment_type',
            lookup_field='id'
        )
        fields = ('id', 'merchant_name', 'account_number', 'expiration_date', 'customer')
        depth = 1


class PaymentTypes(ViewSet):

    def create(self, request):
        """ POST a PaymentType """

        customer = Customer.objects.get(pk=request.data['customer_id'])
        payment_type = PaymentType.objects.create(
            merchant_name = request.data['merchant_name'],
            account_number = request.data['account_number'],
            expiration_date = request.data['expiration_date'],
            customer = customer,
        )

        serializer = PaymentTypeSerializer(payment_type, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """ GET a PaymentType """

        try:
            payment_type = PaymentType.objects.get(pk=pk)
            serializer = PaymentTypeSerializer(payment_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """ PUT a PaymentType """
        
        # attraction = Attraction.objects.get(pk=pk)
        # area = ParkArea.objects.get(pk=request.data["area_id"])
        # attraction.name = request.data["name"]
        # attraction.area = area
        # attraction.save()

        # return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """ DELETE a PaymentType """
        
        # try:
        #     area = Attraction.objects.get(pk=pk)
        #     area.delete()

        #     return Response({}, status=status.HTTP_204_NO_CONTENT)

        # except Attraction.DoesNotExist as ex:
        #     return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        # except Exception as ex:
        #     return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """ GET all PaymentTypes """
        
        # attractions = Attraction.objects.all()

        # # Support filtering attractions by area id
        # area = self.request.query_params.get('area', None)
        # if area is not None:
        #     attractions = attractions.filter(area__id=area)

        # serializer = AttractionSerializer(
        #     attractions, many=True, context={'request': request})
        # return Response(serializer.data)