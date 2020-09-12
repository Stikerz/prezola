import json
from django.core.management.base import BaseCommand, CommandError
from wedding_list.models import Product
import os


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--json_file",
            "-j",
            dest="json_file",
            type=str,
            action="store",
            required=True,
            help="",
        )

    def handle(self, *args, **options):
        file = options["json_file"]
        if os.path.isfile(file.strip()):
            with open(options["json_file"]) as f:
                product_list = json.load(f)

            for product in product_list:
                Product.objects.get_or_create(**product)
        else:
            raise CommandError(f'file {options["json_file"]} does not exist')
