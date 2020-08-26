import json
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapp.models import Product, Customer, ProductType


@csrf_exempt
def search_products(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''

    req_body = json.loads(request.body.decode())

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Use the built-in authenticate method to verify
        keywords = req_body['keywords']

        product_search_list = Product.objects.filter(title__contains=keywords)
        
        serializer = CustomerSerializer(customers, many=True, context={'request': request})



        # # If authentication was successful, respond with their token
        # if authenticated_user is not None:
        #     token = Token.objects.get(user=authenticated_user)
        #     data = json.dumps({"valid": True, "token": token.key})
        #     return HttpResponse(data, content_type='application/json')

        # else:
        #     # Bad login details were provided. So we can't log the user in.
        #     data = json.dumps({"valid": False})
        #     return HttpResponse(data, content_type='application/json')