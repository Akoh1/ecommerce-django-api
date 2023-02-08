from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from core.models.auth import User, Countries, States, BillingAddress
from core.models.cart import Products
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
import jwt
import factory
from faker import Faker
from dataclasses import dataclass
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from rest_framework.response import Response
from rest_framework import status


class Authenticated:
    def __init__(self, token):
        self.token = token

    def get_decoded_token(self):
        if not self.token:
            raise AuthenticationFailed("Unauthenticated")

        try:
            payload = jwt.decode(self.token, "secret", algorithms=["HS256"])
            return payload

        except jwt.ExpiredSignatureError:
            raise PermissionDenied(detail="Unauthorized", code=403)

    def get_auth_user(self):
        payload = self.get_decoded_token()
        try:
            user = get_object_or_404(User, id=payload["id"])
            return user
        except User.DoesNotExist:
            raise Http404


@dataclass
class PaginateSerializer:
    model_obj: None
    page: int
    page_size: int = settings.FILTER_PAGE_SIZE

    def paginate(self) -> Page:
        paginator = Paginator(self.model_obj, self.page_size)
        try:
            objs = paginator.page(self.page)
        except PageNotAnInteger:
            objs = paginator.page(1)
        except EmptyPage:
            objs = paginator.page(paginator.num_pages)
        return objs


fake = Faker()


class RandomProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Products

    title = factory.Faker("sentence", nb_words=2, variable_nb_words=True)
    price = 200
    stock = 10
    description = factory.Faker("sentence", nb_words=20, variable_nb_words=True)
    # group = factory.SubFactory(GroupFactory)


class RandomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = fake.first_name()
    last_name = fake.last_name()
    username = factory.Sequence(lambda n: "john%s" % n)
    email = factory.LazyAttribute(lambda o: "%s@gmail.com" % o.username)
    # password = "password"


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Countries


class StateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = States


class BillingAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BillingAddress
