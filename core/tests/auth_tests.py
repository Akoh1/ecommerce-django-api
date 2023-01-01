from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from core.models.auth import User, Countries
from django.test import RequestFactory
from core.helpers import CountryFactory, StateFactory
from django.shortcuts import get_object_or_404


# Create your tests here.
class AuthenticationTests(APITestCase):
    def setUp(self):
        self.country = CountryFactory.create(name="Nigeria", abbr="NG")
        self.country1 = CountryFactory.create(name="Uganda", abbr="UG")
        self.state = StateFactory.create(country=self.country, name="Lagos", abbr="LG")

    def test_register_user(self):
        url = reverse('register')
        data = {
            'first_name': 'Test',
            'last_name': 'Test',
            'username': 'test',
            'email': "test@gmail.com",
            'password': "xxxx"
        }
        response = self.client.post(url, data, format='json')
        # print(f"res: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get().email, 'test@gmail.com')

    def test_login_user_success(self):
        self.test_register_user()
        url = reverse('login')
        data = {
            'email': "test@gmail.com",
            'password': "xxxx"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "success")
        self.assertIn("jwt", response.data)

    def test_login_user_failed(self):
        self.test_register_user()
        url = reverse('login')
        data = {
            'email': "test@gmail.com",
            'password': "xxx"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_user_success(self):
        self.test_login_user_success()
        url = reverse('user')

        response = self.client.get(url, format='json')
        self.assertEqual(response.data['email'], 'test@gmail.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_billing_address_with_wrong_state(self):
        self.test_view_user_success()
        url = reverse('billing-address')
        data = {
            'street': "37 Ogundola",
            'state': self.state.id,
            'country': self.country1.id,
            'city': "Bariga",
            'zip_code': "100223"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['non_field_errors'][0], 'This state cannot be found in this country')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_billing_address_success(self):
        self.test_view_user_success()
        url = reverse('billing-address')
        data = {
            'street': "37 Ogundola",
            'state': self.state.id,
            'country': self.country.id,
            'city': "Bariga",
            'zip_code': "100223"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['street'], '37 Ogundola')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tearDown(self):
        self.state.delete()
        self.country.delete()


