from django.test import client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from customers.models import Customer
from users.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token



class CustomerTests(APITestCase):

    def setUp(self):

        self.url = reverse('create-customer') # '/api/v1/cutomers/create'

        self.valid_payload = {
            "id": 1,
            "first_name":"Sam",
            "middle_name":"",
            "last_name":"Kay",
            "phone":"0556581926",
            "email":"userr2@gmail.com",
            "address":"1 Cresecent Road",
            "city": "Accra",
            "credit_limit": 500.00,
            "description": "Regular Nivea Lotion Customer"
        }

        self.invalid_payload = {
            "id": "",
            "first_name":"Sam",
            "middle_name":"",
            "last_name":"Kay",
            "phone":"0556581926",
            "email":"userr2@gmail.com",
            "address":"1 Cresecent Road",
            "city": "Accra",
            "credit_limit": 500.00,
            "description": "Regular Nivea Lotion Customer"
        }

    def test_create_customer(self):
        """
        Ensure we can create a new customer.
        """
        response = self.client.post(self.url, self.valid_payload, secure=True, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().first_name, 'Sam')
    

    def tearDown(self) -> None:
        return super().tearDown()