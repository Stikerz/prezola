from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.fields import CurrentUserDefault
from wedding_list.models import Product, WeddingList


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "username": {"required": False},
        }
        fields = ["username", "first_name", "last_name", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user_instance = User(**validated_data)
        user_instance.set_password(password)
        user_instance.save()
        return user_instance

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "brand", "price", "in_stock_quantity"]


def validate_data(quantity, purchased, product):
    if quantity > product.in_stock_quantity:
        raise serializers.ValidationError(
            f"Only {product.in_stock_quantity} currently in stock"
        )


class WeddingListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=CurrentUserDefault()
    )

    product_name = serializers.CharField(source="product", read_only=True)

    class Meta:
        model = WeddingList
        fields = ["id", "user", "product", "quantity", "purchased", "product_name"]

    def get_data(self, data, product=None):
        quantity = 0
        purchased = 0
        if product is None:
            product = data["product"]
        if "quantity" in data:
            quantity = data["quantity"]
        if "purchased" in data:
            purchased = data["purchased"]
        validate_data(quantity, purchased, product)
        return quantity, purchased, product

    def create(self, data):
        user = None
        quantity, purchased, product = self.get_data(data)
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        wl_instance = WeddingList(
            user=user, product=product, quantity=quantity, purchased=purchased
        )
        wl_instance.save()
        product.in_stock_quantity -= purchased
        product.save()
        return wl_instance

    def update(self, instance, data):
        quantity, purchased, product = self.get_data(data, instance.product)
        purchase_diff = 0
        instance.quantity = quantity
        if instance.purchased < purchased:
            purchase_diff = purchased - instance.purchased
            if purchase_diff > quantity:
                raise serializers.ValidationError(
                    f"Cannot purchase more than whats in your list"
                )
        instance.quantity -= purchase_diff
        instance.purchased = purchased
        product.in_stock_quantity -= purchase_diff
        product.save()
        instance.save()
        return instance
