import json
from django.http import HttpResponse
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from bangazonapp.models import Customer


class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'
        )
        fields = ('id', 'address', 'phone_number', 'user')
        depth = 2


class Customers(ViewSet):
    """Park Areas for Kennywood Amusement Park"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized User instance
        """

        user = User.objects.create_user(
            first_name=request.data["first_name"],
            last_name=request.data["last_name"],
            username=request.data["username"],
            password=request.data["password"],
            email=request.data["email"]
        )

        customer = Customer.objects.create(
            address=request.data["address"],
            phone_number=request.data["phone_number"],
            user=user
        )

        token = Token.objects.create(user=user)

        data = json.dumps({"token": token.key})
        return HttpResponse(data, content_type='application/json')

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            # user = User.objects.get(pk=pk)
            customer = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(
                customer, context={'request': request})
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
        if request.user.id:
            customers = Customer.objects.filter(user=request.user.id)
        else:
            customers = Customer.objects.all()
        serializer = CustomerSerializer(
            customers, many=True, context={'request': request})
        return Response(serializer.data)
