from rest_framework import serializers
from .models import Category, Item
from drf_haystack.serializers import HaystackSerializer
from .search_indexes import ItemIndex, CategoryIndex


class CategoryListSerializer(serializers.ModelSerializer):
    """
    Category List serializer
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


class CategoryListHaystackSerializer(HaystackSerializer):
    """
    Category List serializer
    """
    class Meta:
        index_classes = [CategoryIndex]
        fields = ['id', 'name', 'parent']


class CategoryAddSerializer(serializers.ModelSerializer):
    """
    Add category
    """
    class Meta:
        model = Category
        fields = ['name', 'parent']


class ItemDetailSerializer(serializers.ModelSerializer):
    """
    Detail Item
    Get by id
    """
    category = CategoryListSerializer()

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


class ItemListHaystackSerializer(HaystackSerializer):
    """
    List of Items
    Get by category
    """
    class Meta:
        index_classes = [ItemIndex]
        fields = [
            "name", "price", "category", "image_url", "description", "id"
        ]


