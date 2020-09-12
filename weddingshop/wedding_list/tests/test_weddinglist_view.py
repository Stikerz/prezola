from rest_framework.utils import json
from rest_framework import status
from django.core.management import call_command
from django.test import TestCase
import os
from weddingshop import settings
from wedding_list.tests.support.assertions import assert_valid_schema
from django.contrib.auth.models import User
from wedding_list.models import WeddingList, Product

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
        product_instance = Product.objects.get(id=1)
        WeddingList(
            user=user_instance, product=product_instance, quantity=1, purchased=1
        ).save()

    def login(self) -> bool:
        user_login = self.client.login(
            username=self.user_data["username"], password="gamora"
        )
        return user_login

    def test_get_list(self):
        user_login = self.login()
        self.assertTrue(user_login)
        response = self.client.get("/weddingshop/list/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        assert_valid_schema(response.json(), "list_schema.json")

    def test_add_list_gift(self):
        user_login = self.login()
        self.assertTrue(user_login)
        initial_stock = Product.objects.get(id=2).in_stock_quantity
        data = {
            "user": 1,
            "product": 2,
            "quantity": 1,
            "purchased": 1,
        }
        response = self.client.post(
            "/weddingshop/list/",
            data=json.dumps(data),
            content_type="application/json",
        )
        post_stock = Product.objects.get(id=2).in_stock_quantity
        self.assertEqual(post_stock, initial_stock - 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response2 = self.client.get("/weddingshop/list/")
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.data), 2)

    def test_stock_error_add_list_gift(self):
        user_login = self.login()
        self.assertTrue(user_login)
        data = {
            "user": 1,
            "product": 2,
            "quantity": 10,
            "purchased": 10,
        }
        response = self.client.post(
            "/weddingshop/list/",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[0], "Only 5 currently in stock")

    def test_delete_gift(self):
        user_login = self.login()
        self.assertTrue(user_login)
        response = self.client.delete("/weddingshop/listitem/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response2 = self.client.get("/weddingshop/list/")
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(response2.data), 0)
