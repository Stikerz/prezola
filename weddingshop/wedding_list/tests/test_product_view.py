from rest_framework.utils import json
from rest_framework import status
from django.core.management import call_command
from django.test import TestCase
import os
from weddingshop import settings
from wedding_list.tests.support.assertions import assert_valid_schema
from django.contrib.auth.models import User

DATA_DIR = os.path.join(
    os.path.split(settings.BASE_DIR)[0],
    "weddingshop",
    "wedding_list",
    "tests",
    "support",
    "data",
)


class ProductViewTest(TestCase):
    def setUp(self):
        file_path = os.path.join(DATA_DIR, "sample_products.json")
        call_command("addproducts", json_file=file_path)
        self.user_data = {
            "username": "marvel",
            "first_name": "black",
            "last_name": "panther",
        }
        user_instance = User(**self.user_data)
        user_instance.set_password("gamora")
        user_instance.save()

    def login(self) -> bool:
        user_login = self.client.login(
            username=self.user_data["username"], password="gamora"
        )
        return user_login

    def test_get_products(self):
        user_login = self.login()
        self.assertTrue(user_login)
        response = self.client.get("/weddingshop/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        assert_valid_schema(response.json(), "products_schema.json")

    def test_unauthorized_get_products(self):
        response = self.client.get("/weddingshop/products/")
        self.assertEqual(response.status_code, 401)

    def test_create_product(self):
        user_login = self.login()
        self.assertTrue(user_login)
        new_product_data = {
            "name": "Glow Challenger T2 Square Parasol - 3m, Taupe,",
            "brand": "GARDENSTORE",
            "price": 619.99,
            "in_stock_quantity": 30,
        }
        response = self.client.post(
            "/weddingshop/products/",
            data=json.dumps(new_product_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_create_product(self):
        user_login = self.login()
        self.assertTrue(user_login)
        new_product_data = {
            "name": "",
            "brand": "",
            "price": "",
            "in_stock_quantity": "30",
        }
        response = self.client.post(
            "/weddingshop/products/",
            data=json.dumps(new_product_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
