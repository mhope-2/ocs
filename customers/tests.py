from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Customer

class CustomerTests(APITestCase):
    def test_create_customer(self):
        """
        Ensure we can create a new customer object.
        """
        url = reverse('customers:customers-add')
        data = {'name': 'DabApps'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Account.objects.get().name, 'DabApps')


