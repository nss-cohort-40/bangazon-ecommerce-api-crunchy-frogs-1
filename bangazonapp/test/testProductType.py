import json
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from bangazonapp.models import ProductType
from rest_framework.authtoken.models import Token

class TestProductType(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'foobar'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)

    def test_post_producttype(self): 

        new_producttype = { 
            "name": "Electronics"
        }

        response = self.client.post(
            reverse('producttype-list'), new_producttype, HTTP_AUTHORIZATION='Token' + str(self.token)
        )

        self.assertEqual(response.status_code, 200)

        self.assertAlmostEqual(ProductType.objects.count(), 1)

        self.assertEqual(ProductType.objects.get().name, "Electronics")

    def test_get_producttype(self):

        new_producttype = ProductType.objects.create(
            name="Electronics"
        )

        response = self.client.get(reverse('producttype-list'))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]["name"], "Electronics")

        self.assertIn(new_producttype.name.encode(), response.content)