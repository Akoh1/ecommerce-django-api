import http
from urllib import response
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from core.models.auth import User, BillingAddress, States, Countries
from ..serializers.auth import UserSerializer, BillAddressSerializer, StateSerializer, CountrySerializer
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from django.contrib.auth import authenticate
from ..helpers import Authenticated

# Create your views here.


def index(request):
    return HttpResponse("Hello, world!")


class StateList(generics.ListAPIView):
    queryset = States.objects.all()
    serializer_class = StateSerializer


class CountryList(generics.ListAPIView):
    queryset = Countries.objects.all()
    serializer_class = CountrySerializer


class RegisterView(APIView):
    # renderer_classes = (UserJSONRenderer,)
    # def get(self, request, format=None):
    #     snippets = Snippet.objects.all()
    #     serializer = SnippetSerializer(snippets, many=True)
    #     return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request, format=None):
        email = request.data['email']
        password = request.data['password']
        # print(f"email: {email}, password: {password}")

        # user = User.objects.filter(email=email).first()
        user = authenticate(username=email, password=password)

        if user is None:
            raise AuthenticationFailed("user not found")

        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        # token = jwt.decode(encoded, "secret", algorithms=["HS256"])
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            "message": "success",
            "jwt": token
        }
        return response


class UserView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        token = request.COOKIES.get('jwt')
        authenticated = Authenticated(token)
        # user = get_object_or_404(User, id=payload['id'])
        user = authenticated.get_auth_user()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response =  Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "success"
        }
        return response


class BillingAddressView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    renderer_classes = [JSONRenderer]

    def get_object(self, token):
        user = Authenticated(token).get_auth_user()

        try:
            return BillingAddress.objects.filter(user=user.id)
        except BillingAddress.DoesNotExist:
            raise Http404

    def get(self, request):
        token = request.COOKIES.get('jwt')

        items = self.get_object(token)

        serializer = BillAddressSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        token = request.COOKIES.get('jwt')
        user = Authenticated(token).get_auth_user()

        data = request.data
        data['user'] = user.id
        serializer = BillAddressSerializer(data=data)



        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


