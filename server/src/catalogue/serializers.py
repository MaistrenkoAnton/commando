from rest_framework import serializers
from .models import Category, Item


class CategoryListSerializer(serializers.ModelSerializer):
    """
    Category List serializer
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


class CategoryAddSerializer(serializers.ModelSerializer):
    """
    Add category
    """
    class Meta:
        model = Category
        fields = ['name', 'parent']


class ItemListSerializer(serializers.ModelSerializer):
    """
    List of Items
    Get by category
    """
    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'image_url', 'category']


class ItemDetailSerializer(serializers.ModelSerializer):
    """
    Detail Item
    Get by id
    """
    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'category', 'description', 'image_url']


class ItemAddSerializer(serializers.ModelSerializer):
    """
    Add Item
    """
    class Meta:
        model = Item
        fields = ['name', 'price', 'category', 'description', 'image_url']
