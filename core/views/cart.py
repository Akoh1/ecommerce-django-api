from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from core.models.cart import Products, OrderItem, Cart
from core.models.auth import BillingAddress, User
from core.serializers.cart import ProductsSerializer, StandardResultsSetPagination, OrderItemSerializer, CartSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import AuthenticationFailed
from ..helpers import Authenticated, PaginateSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.conf import settings
from django.db import transaction
from datetime import datetime
from django.utils import timezone
from typing import List


class ProductList(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    pagination_class = StandardResultsSetPagination


class OrderItemsList(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    pagination_class = StandardResultsSetPagination


class OrderItemsView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    renderer_classes = [JSONRenderer]

    def get_object(self, token):
        user = Authenticated(token).get_auth_user()

        try:
            return OrderItem.objects.filter(user=user.id)
        except OrderItem.DoesNotExist:
            raise Http404

    def get(self, request):
        token = request.COOKIES.get('jwt')
        page = self.request.query_params.get('page ', 1)
        # page_size = self.request.query_params.get('page_size ', 10)

        items = self.get_object(token)
        objs = PaginateSerializer(items, page)
        paginate_objs = objs.paginate()

        serializer = OrderItemSerializer(paginate_objs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request, format=None):
    #     token = request.COOKIES.get('jwt')
    #     user = Authenticated(token).get_auth_user()
    #
    #     data = request.data
    #     data['user'] = user.id
    #     serializer = CommentSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class CommentDetailView(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     renderer_classes = [JSONRenderer]
#
#     def get_object(self, pk, token):
#         user = Authenticated(token).get_auth_user()
#
#         try:
#             return Comment.objects.get(pk=pk, user=user.id)
#         except Comment.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         token = request.COOKIES.get('jwt')
#
#         comment = self.get_object(pk, token)
#         serializer = CommentSerializer(comment)
#         return Response(serializer.data)
#
#     def patch(self, request, pk, format=None):
#         token = request.COOKIES.get('jwt')
#
#         comment = self.get_object(pk, token)
#         serializer = CommentSerializer(comment, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         token = request.COOKIES.get('jwt')
#         comment = self.get_object(pk, token)
#         comment.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class CartView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    renderer_classes = [JSONRenderer]

    def get_object(self, token):
        user = Authenticated(token).get_auth_user()

        try:
            return Cart.objects.filter(user=user.id)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request):
        token = request.COOKIES.get('jwt')
        page = self.request.query_params.get('page ', 1)
        # page_size = self.request.query_params.get('page_size ', 10)

        items = self.get_object(token)
        objs = PaginateSerializer(items, page)
        paginate_objs = objs.paginate()

        serializer = CartSerializer(paginate_objs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        token = request.COOKIES.get('jwt')
        user = Authenticated(token).get_auth_user()

        data = request.data
        print(f"getting original data: {data}")

        user_billing_address = BillingAddress.objects.filter(user=user.id)

        if bool(user_billing_address) is False:
            error = {
                "error": "No billing address"
            }
            return Response(error, status=status.HTTP_404_NOT_FOUND)

        # get active user billing address
        active_billing_address = get_object_or_404(BillingAddress, user=user.id, to_use=True)
        print(f"Callimg post cart: {active_billing_address}")
        data['bill_address'] = active_billing_address.id

        # get product instance from product slug and create and get or create order item
        with transaction.atomic():
            data["user"] = user.id
            product_slug = data.pop('product_slug', None)
            product = get_object_or_404(Products, slug=product_slug)
            order_item, item_created = OrderItem.objects.get_or_create(
                user=user, product=product, ordered=False
            )
            data["items"]: List[OrderItem] = [order_item]
            # for prod_slug in product_slug:
            #     product = get_object_or_404(Products, slug=prod_slug)
            #     order_item, item_created = OrderItem.objects.get_or_create(
            #         user=user, product=product, ordered=False
            #     )
            # data["items"].append(order_item)
            # check if user already has an open cart
            my_cart = Cart.objects.filter(user=user.id, ordered=False)
            output = {}
            # with transaction.atomic():
            if my_cart.exists():
                print("cart exists")
                cart = my_cart[0]
                # get the first instance of cart
                # check if order item for product already exists in cart
                # if order item exists then increase oder item count for cart
                # save cart object
                # else add order item to cart
                serializer = CartSerializer(cart, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(f"cart does not exist")
                # create new cart with order items
                output["cart"] = "User has no cart"
                data['ordered_date'] = datetime.now()

                print(f"post data: {data}")
                serializer = CartSerializer(data=data, context={'request': request})

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
