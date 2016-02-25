from rest_framework import serializers
from .models import Cart


class CartAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['user', 'item']


class CartListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['user', 'item', 'purchase_time']