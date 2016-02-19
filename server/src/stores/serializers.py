from rest_framework import serializers
from .models import Store, StoreItem
from catalogue.serializers import ItemAddSerializer, ItemDetailSerializer, CategoryListSerializer


class StoreListSerializer(serializers.ModelSerializer):
    """
    Store List serializer
    """
    class Meta:
        model = Store
        fields = ['id', 'title', 'margin', 'activity_status']


class StoreItemDetailSerializer(serializers.ModelSerializer):
    """
    Detail StoreItem
    Get by id
    """
    category = CategoryListSerializer()
    store = StoreListSerializer

    class Meta:
        model = StoreItem
        fields = ['id', 'name', 'price', 'category', 'description', 'image_url', 'comments_total', 'average_rate',
                  'store', 'quantity', 'running_out_level', 'running_out']


class StoreItemAddSerializer(serializers.ModelSerializer):
    """
    Add Item
    """
    class Meta:
        model = StoreItem
        fields = ['name', 'price', 'category', 'description', 'image_url', 'comments_total', 'average_rate',
                  'store', 'quantity', 'running_out_level', 'running_out']