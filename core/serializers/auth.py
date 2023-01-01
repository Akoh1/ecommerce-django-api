from rest_framework import serializers
from ..models.auth import User, BillingAddress, Countries, States
from django.shortcuts import get_object_or_404


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = ['id', 'name', 'abbr']


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = ['id', 'country', 'name', 'abbr']


class BillAddressSerializer(serializers.ModelSerializer):
    # country = CountrySerializer()
    # state = StateSerializer()

    class Meta:
        model = BillingAddress
        fields = ['id', 'user', 'street', 'state', 'country', 'city', 'zip_code', 'to_use']

    def validate(self, data):
        """
        Check that State has a correct relationship to Country.
        """
        if data['state'].country.id != data['country'].id:
            raise serializers.ValidationError("This state cannot be found in this country")
        return data


class BillAddressSerializerParser(serializers.ModelSerializer):
    # country = CountrySerializer()
    # state = StateSerializer()

    class Meta:
        model = BillingAddress
        fields = ['id']
