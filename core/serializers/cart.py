from rest_framework import serializers, pagination
from core.models.cart import Products, OrderItem, Cart
from .auth import UserSerializer, BillAddressSerializer, BillAddressSerializerParser
from datetime import datetime
from typing import Dict, Any
from django.shortcuts import get_object_or_404


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'title', 'price', 'stock', 'description', 'image', 'slug']


class OrderItemSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductsSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'user', 'product', 'ordered', 'num_of_prod', 'total_price']


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id']


class CartSummarySerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    items = OrderItemSerializer(read_only=True, many=True)
    # bill_address = BillAddressSerializerParser(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'start_date', 'ordered_date', 'ordered', 'bill_address', 'total_amount']


class CartSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    items = ItemSerializer(read_only=True, many=True)
    # bill_address = BillAddressSerializerParser(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'start_date', 'ordered_date', 'ordered', 'bill_address', 'total_amount']

    def create(self, validated_data):
        request = self.context['request']
        print(f"request: {request.data}")
        items_data = request.data.get("items")
        validated_data["items"] = items_data
        print(f"valid data: {validated_data}")
        #
        # order_pk = request.data.get('order')
        # order_pk = attempt_json_deserialize(order_pk, expect_type=str)
        # validated_data['order_id'] = order_pk
        #
        # box_data = request.data.get('box')
        # box_data = attempt_json_deserialize(box_data, expect_type=dict)
        # box = Box.objects.create(**box_data)
        # validated_data['box'] = box
        #
        # toppings_data = request.data.get('toppings')
        # # toppings_data = attempt_json_deserialize(toppings_data, expect_type=list)
        # # validated_data['toppings'] = toppings_data
        # toppings_objs = [Topping.objects.create(**data) for data in toppings_data]
        # validated_data['toppings'] = toppings_objs

        instance = super().create(validated_data)

        return instance

    def update(self, instance, validated_data):
        request = self.context['request']
        print(f"serilizer request: {request.data}")
        product_slug = request.data.get("product_slug")
        items_data = request.data.get("items")
        print(f"update cart items: {instance.id}")
        print(f"instance cart items: {instance.items}")
        user = validated_data.get("user")
        # product = get_object_or_404(Products, slug=product_slug)
        # print(f"product : {product}")
        # order_item =
        # if OrderItem.objects.filter(product__slug=product_slug).exists():
        # if instance.items.filter(product__slug=product_slug).exists():
        #     print(f"product in cart already")
        #
        #     instance.items.num_of_prod += 1
        #     # instance.items.num_of_prod += 1
        #     # instance.items.save()
        # else:
        instance.items.add(items_data[0])
        # validated_data["items"] = items_data
        print(f"valid data: {validated_data}")
        # instance.title = validated_data.get('title', instance.title)
        # instance.code = validated_data.get('code', instance.code)
        # instance.linenos = validated_data.get('linenos', instance.linenos)
        # instance.language = validated_data.get('language', instance.language)
        # instance.style = validated_data.get('style', instance.style)
        instance.save()

        # order_data = request.data.get('order')
        # order_data = attempt_json_deserialize(order_data, expect_type=str)
        # validated_data['order_id'] = order_data
        #
        # box_data = request.data.get('box')
        # box_data = attempt_json_deserialize(box_data, expect_type=dict)
        # box = Box.objects.create(**box_data)
        # validated_data['box'] = box
        #
        # toppings_data = request.data.get('toppings')
        # toppings_ids = attempt_json_deserialize(toppings_data, expect_type=list)
        # validated_data['toppings'] = toppings_ids

        # instance = super().update(instance, validated_data)

        return instance
