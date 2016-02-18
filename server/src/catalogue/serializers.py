from rest_framework import serializers
from .models import Category, Item, Comment, Rate


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
        fields = ['id', 'name', 'price', 'image_url', 'category', 'comments_total', 'average_rate']


class ItemDetailSerializer(serializers.ModelSerializer):
    """
    Detail Item
    Get by id
    """
    category = CategoryListSerializer()

    class Meta:
        model = Item
        fields = ['id', 'name', 'price', 'category', 'description', 'image_url', 'comments_total', 'average_rate']


class ItemAddSerializer(serializers.ModelSerializer):
    """
    Add Item
    """
    class Meta:
        model = Item
        fields = ['name', 'price', 'category', 'description', 'image_url']


class CommentAddSerializer(serializers.ModelSerializer):
    """
    Add comment
    """
    class Meta:
        model = Comment
        fields = ['text', 'item', 'user']


class RateAddSerializer(serializers.ModelSerializer):
    """
    Add rate
    """
    class Meta:
        model = Rate
        fields = ['rate', 'item', 'user']
