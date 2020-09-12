from django.db import models, Error
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Product(models.Model):

    name = models.CharField(max_length=100, blank=False, null=False)
    brand = models.CharField(max_length=100, blank=False, null=False)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    in_stock_quantity = models.IntegerField(
        default=0, validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.name


class WeddingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    purchased = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="unique_product")
        ]
