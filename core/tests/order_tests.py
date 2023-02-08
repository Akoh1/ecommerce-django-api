from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from core.models.auth import User
from core.models.cart import Products, OrderItem, Cart
from django.test import RequestFactory
from core.helpers import (
    RandomProductFactory,
    RandomUserFactory,
    CountryFactory,
    StateFactory,
    BillingAddressFactory,
)


class OrderTests(APITestCase):
    def setUp(self):
        self.products = []
        for i in range(5):
            product = RandomProductFactory.create()
            product.save()
            self.products.append(product)
        # self.user = RandomUserFactory.create()
        # self.user.set_password('password')
        reg_url = reverse("register")
        data = {
            "first_name": "Test",
            "last_name": "Test",
            "username": "test",
            "email": "test@gmail.com",
            "password": "xxxx",
        }
        self.client.post(reg_url, data, format="json")
        self.country = CountryFactory.create(name="Nigeria", abbr="NG")
        self.state = StateFactory.create(country=self.country, name="Lagos", abbr="LG")

    def test_get_products(self):
        url = reverse("products")

        response = self.client.get(url, format="json")
        # print(f"Res: {response.data}")
        self.assertEqual(len(response.data["results"]), 5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_to_cart_without_billing_address(self):
        login_url = reverse("login")
        data = {"email": "test@gmail.com", "password": "xxxx"}
        res = self.client.post(login_url, data, format="json")
        cart_url = reverse("add-to-cart")
        cart_data = {}
        response = self.client.post(cart_url, cart_data, format="json")
        self.assertEqual(response.data["error"], "No billing address")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_to_cart_with_billing_address_no_cart_currently(self):
        login_url = reverse("login")
        data = {"email": "test@gmail.com", "password": "xxxx"}
        self.client.post(login_url, data, format="json")
        data = {"email": "test@gmail.com", "password": "xxxx"}
        self.client.post(login_url, data, format="json")
        address_url = reverse("billing-address")
        data = {
            "street": "37 Ogundola",
            "state": self.state.id,
            "country": self.country.id,
            "city": "Bariga",
            "zip_code": "100223",
            "to_use": True,
        }
        self.client.post(address_url, data, format="json")
        cart_url = reverse("add-to-cart")
        cart_data = {
            "product_slug": self.products[0].slug,
        }

        response = self.client.post(cart_url, cart_data, format="json")

        self.assertTrue(response.data["id"])
        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_to_cart_with_billing_address_cart_exists_same_product(self):
        login_url = reverse("login")
        data = {"email": "test@gmail.com", "password": "xxxx"}
        self.client.post(login_url, data, format="json")
        data = {"email": "test@gmail.com", "password": "xxxx"}
        self.client.post(login_url, data, format="json")
        address_url = reverse("billing-address")
        data = {
            "street": "37 Ogundola",
            "state": self.state.id,
            "country": self.country.id,
            "city": "Bariga",
            "zip_code": "100223",
            "to_use": True,
        }
        self.client.post(address_url, data, format="json")
        cart_url = reverse("add-to-cart")
        cart_data = {
            "product_slug": self.products[0].slug,
        }

        response = self.client.post(cart_url, cart_data, format="json")
        n_cart_data = {
            "product_slug": self.products[0].slug,
        }
        response = self.client.post(cart_url, n_cart_data, format="json")
        s_cart_data = {
            "product_slug": self.products[0].slug,
        }
        response = self.client.post(cart_url, s_cart_data, format="json")
        total_amount = self.products[0].price * 3
        order_items = OrderItem.objects.get(id=response.data["items"][0].get("id"))
        cart = Cart.objects.get(id=response.data["id"])
        # self.assertTrue(response.data['id'])
        self.assertEqual(order_items.num_of_prod, 3)
        self.assertEqual(response.data["total_amount"], total_amount)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_to_cart_with_billing_address_cart_exists_different_products(self):
        login_url = reverse("login")
        data = {"email": "test@gmail.com", "password": "xxxx"}
        self.client.post(login_url, data, format="json")
        data = {"email": "test@gmail.com", "password": "xxxx"}
        self.client.post(login_url, data, format="json")
        address_url = reverse("billing-address")
        data = {
            "street": "37 Ogundola",
            "state": self.state.id,
            "country": self.country.id,
            "city": "Bariga",
            "zip_code": "100223",
            "to_use": True,
        }
        self.client.post(address_url, data, format="json")
        cart_url = reverse("add-to-cart")
        cart_data = {
            "product_slug": self.products[0].slug,
        }

        response = self.client.post(cart_url, cart_data, format="json")
        n_cart_data = {
            "product_slug": self.products[1].slug,
        }
        response = self.client.post(cart_url, n_cart_data, format="json")

        s_cart_data = {
            "product_slug": self.products[2].slug,
        }

        response = self.client.post(cart_url, s_cart_data, format="json")

        total_amount = (
            self.products[0].price + self.products[1].price + self.products[2].price
        )

        self.assertEqual(len(response.data["items"]), 3)
        self.assertEqual(response.data["total_amount"], total_amount)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def tearDown(self):
        for prod in self.products:
            prod.delete()
        # self.user.delete()
