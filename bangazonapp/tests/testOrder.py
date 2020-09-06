import json
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from bangazonapp.models import Order
from bangazonapp.models import Customer
from bangazonapp.models import PaymentType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# *  Good rules-of-thumb include having:
#     * a separate TestClass for each model or view, or for us --- every endpoint
#     * a separate test method for each set of conditions you want to test
#     * test method names that describe their function

class TestOrder(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(
            address="9 Street",
            phone_number="8888888888",
            user=User.objects.create_user({
                "username": "spork",
                "password": "spokr"
            })
        )
        self.payment_type = PaymentType.objects.create(
            merchant_name='VISA',
            account_number='2222545490992211',
            expiration_date='2020-11-01',
            customer=self.customer
        )
        self.token = Token.objects.create(user=self.customer.user)

    def test_post_order(self):

        new_order = {
              "customer": self.customer,
            }

        response = self.client.post(
            reverse('order-list'), new_order, HTTP_AUTHORIZATION='Token ' + str(self.token)
          )
    
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().customer, self.customer)

    # def test_get_parkareas(self):

    #     new_area = ParkArea.objects.create(
    #       name="Coaster Land",
    #       theme="coasters, duh",
    #     )

    #     # Now we can grab all the area (meaning the one we just created) from the db
    #     response = self.client.get(reverse('parkarea-list'))

    #     # Check that the response is 200 OK.
    #     # This is checking for the GET request result, not the POST. We already checked that POST works in the previous test!
    #     self.assertEqual(response.status_code, 200)

    #     # response.data is the python serialized data used to render the JSON, while response.content is the JSON itself.
    #     # Are we responding with the data we asked for? There's just one parkarea in our dummy db, so it should contain a list with one instance in it
    #     self.assertEqual(len(response.data), 1)

    #     # test the contents of the data before it's serialized into JSON
    #     self.assertEqual(response.data[0]["name"], "Coaster Land")

    #     # Finally, test the actual rendered content as the client would receive it.
    #     # .encode converts from unicode to utf-8. Don't get hung up on this. It's just how we can compare apples to apples
    #     self.assertIn(new_area.name.encode(), response.content)