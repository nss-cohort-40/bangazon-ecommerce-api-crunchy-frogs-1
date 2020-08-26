from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapp.models import ProductType


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductType
        url = serializers.HyperlinkedIdentityField(
            view_name='producttype',
            lookup_field='id'
        )
        fields = ('id', 'name', 'url')


class ProductTypes(ViewSet):

    def create(self, request):

        new_product_type = ProductType()
        new_product_type.name = request.data['name']
        new_product_type.save()

        serializer = ProductTypeSerializer(
            new_product_type, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            product_type = ProductType.objects.get(pk=pk)
            serializer = ProductTypeSerializer(
                product_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        product_type = ProductType.objects.get(pk=pk)
        product_type.name = request.data["name"]
        product_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):

        try:
            product_type = ProductType.objects.get(pk=pk)
            product_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ProductType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            product_types = ProductType.objects.all()

            serializer = ProductTypeSerializer(
                product_types, many=True, context={'request': request})
            return Response(serializer.data)
        except:
            return HttpResponseServerError(Exception)
