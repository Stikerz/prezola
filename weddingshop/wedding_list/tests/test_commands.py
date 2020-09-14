from django.core.management import call_command
from django.test import TestCase
import os
from weddingshop import settings
from wedding_list.models import Product
from django.core.management.base import CommandError

DATA_DIR = os.path.join(
    os.path.split(settings.BASE_DIR)[0],
    "weddingshop",
    "wedding_list",
    "tests",
    "support",
    "data",
)


class AddStoresTest(TestCase):
    def test_command_with_file_path(self):
        self.assertEqual(len(Product.objects.all()), 0)
        file_path = os.path.join(DATA_DIR, "sample_products.json")
        call_command("addproducts", json_file=file_path)

        self.assertEqual(len(Product.objects.all()), 3)

    def test_command_with_invalid_filepath(self):
        self.assertEqual(len(Product.objects.all()), 0)
        file_path = "/fake/foo/path"
        with self.assertRaises(CommandError):
            call_command("addproducts", json_file=file_path)

        self.assertEqual(len(Product.objects.all()), 0)
